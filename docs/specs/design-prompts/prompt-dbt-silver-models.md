# Design Prompt: dbt Silver Layer Models

**Component:** Data Transformation Layer  
**Phase:** 1-2 (Foundation → Core)  
**Priority:** P0 - Critical Path  
**Estimated Effort:** 3-4 days  
**Depends On:** [Bronze Layer Ingestion](prompt-bronze-layer-ingest.md)

---

## Context for Implementation

This prompt guides building the dbt models that transform Bronze (raw) data into Silver (cleaned, validated, typed) data. The Silver layer is where data quality is enforced and the data becomes queryable for analysis.

**Pre-requisites:**
- Bronze layer ingestion working (Iceberg tables populated)
- dbt-core and dbt-duckdb adapter installed
- Understanding of medallion architecture

---

## Objective

Build a dbt project that transforms `bronze.reactor_timeseries_raw` into `silver.reactor_readings`—a clean, typed, deduplicated table ready for analytics and ML training.

Transformations must:
1. **Deduplicate** - Remove duplicate readings (same timestamp + channel)
2. **Type-cast** - Convert strings to appropriate types
3. **Validate** - Flag or filter invalid readings
4. **Enrich** - Add derived columns (hour, day, is_weekday, etc.)
5. **Document** - Full column descriptions and lineage

---

## Project Structure

```
dbt/neutron_os/
├── dbt_project.yml
├── profiles.yml              # Connection to DuckDB + Iceberg
├── packages.yml              # dbt dependencies
│
├── models/
│   ├── staging/              # Light transforms on Bronze
│   │   ├── _staging.yml      # Source definitions
│   │   └── stg_reactor_timeseries.sql
│   │
│   ├── silver/               # Cleaned, validated data
│   │   ├── _silver.yml       # Model configs + tests
│   │   ├── reactor_readings.sql
│   │   ├── channel_metadata.sql
│   │   └── data_quality_log.sql
│   │
│   └── gold/                 # Aggregated metrics (Phase 2)
│       ├── _gold.yml
│       ├── reactor_hourly_metrics.sql
│       └── channel_daily_stats.sql
│
├── macros/
│   ├── quality_checks.sql    # Reusable validation logic
│   └── time_helpers.sql      # Timestamp utilities
│
├── seeds/
│   └── channel_reference.csv # Static channel metadata
│
└── tests/
    ├── assert_no_duplicates.sql
    └── assert_valid_timestamps.sql
```

---

## Model Specifications

### 1. Staging Model: `stg_reactor_timeseries`

Lightweight transform that standardizes the Bronze data:

```sql
-- models/staging/stg_reactor_timeseries.sql

{{
    config(
        materialized='view',
        description='Standardized reactor timeseries from Bronze layer'
    )
}}

with source as (
    select * from {{ source('bronze', 'reactor_timeseries_raw') }}
),

renamed as (
    select
        -- Standardize timestamp (handle both ISO and epoch formats)
        case 
            when event_timestamp like '%T%' 
            then cast(event_timestamp as timestamp)
            else to_timestamp(cast(event_timestamp as bigint) / 1000)
        end as reading_timestamp,
        
        -- Pass through
        channel_id,
        channel_name,
        cast(value as double) as reading_value,
        unit as reading_unit,
        quality_flag,
        
        -- Audit columns
        _source_file,
        _ingestion_ts,
        _batch_id,
        _row_hash
        
    from source
)

select * from renamed
```

### 2. Silver Model: `reactor_readings`

The core Silver table with deduplication and validation:

```sql
-- models/silver/reactor_readings.sql

{{
    config(
        materialized='incremental',
        unique_key='reading_id',
        incremental_strategy='merge',
        partition_by={'field': 'reading_date', 'data_type': 'date'},
        description='Cleaned and validated reactor sensor readings'
    )
}}

with staged as (
    select * from {{ ref('stg_reactor_timeseries') }}
    {% if is_incremental() %}
    where _ingestion_ts > (select max(_ingestion_ts) from {{ this }})
    {% endif %}
),

deduplicated as (
    -- Keep latest ingestion for each timestamp+channel combo
    select
        *,
        row_number() over (
            partition by reading_timestamp, channel_id 
            order by _ingestion_ts desc
        ) as _rn
    from staged
),

validated as (
    select
        -- Generate surrogate key
        {{ dbt_utils.generate_surrogate_key(['reading_timestamp', 'channel_id']) }} as reading_id,
        
        -- Core columns
        reading_timestamp,
        cast(reading_timestamp as date) as reading_date,
        channel_id,
        channel_name,
        reading_value,
        reading_unit,
        
        -- Quality assessment
        quality_flag as source_quality_flag,
        case
            when reading_value is null then 'MISSING'
            when reading_value < 0 and reading_unit in ('kW', 'degC') then 'INVALID'
            when quality_flag = 'BAD' then 'BAD'
            when quality_flag = 'SUSPECT' then 'SUSPECT'
            else 'GOOD'
        end as validated_quality,
        
        -- Time enrichment
        extract(hour from reading_timestamp) as reading_hour,
        extract(dow from reading_timestamp) as reading_dow,
        case when extract(dow from reading_timestamp) in (0, 6) then false else true end as is_weekday,
        
        -- Lineage
        _source_file,
        _ingestion_ts,
        _row_hash,
        current_timestamp as _silver_processed_ts
        
    from deduplicated
    where _rn = 1  -- Dedup
      and reading_value is not null  -- Filter missing
)

select * from validated
```

### 3. Channel Metadata: `channel_metadata`

Reference data for sensor channels:

```sql
-- models/silver/channel_metadata.sql

{{
    config(
        materialized='table',
        description='Channel reference data with measurement ranges'
    )
}}

with seed_data as (
    select * from {{ ref('channel_reference') }}
),

enriched as (
    select
        channel_id,
        channel_name,
        display_name,
        measurement_type,
        unit,
        
        -- Valid ranges for anomaly detection
        min_valid_value,
        max_valid_value,
        
        -- Metadata
        location,
        instrument_model,
        calibration_date,
        
        -- Computed
        current_timestamp as _updated_at
        
    from seed_data
)

select * from enriched
```

### 4. Data Quality Log: `data_quality_log`

Track quality issues for monitoring:

```sql
-- models/silver/data_quality_log.sql

{{
    config(
        materialized='incremental',
        unique_key='issue_id',
        description='Log of data quality issues detected during Silver processing'
    )
}}

with quality_issues as (
    select
        {{ dbt_utils.generate_surrogate_key(['reading_timestamp', 'channel_id', 'issue_type']) }} as issue_id,
        reading_timestamp,
        channel_id,
        reading_value,
        'OUT_OF_RANGE' as issue_type,
        concat('Value ', reading_value, ' outside expected range') as issue_description,
        _source_file,
        current_timestamp as detected_at
    from {{ ref('stg_reactor_timeseries') }}
    where reading_value < (
        select min_valid_value from {{ ref('channel_metadata') }} cm 
        where cm.channel_id = stg_reactor_timeseries.channel_id
    )
    or reading_value > (
        select max_valid_value from {{ ref('channel_metadata') }} cm 
        where cm.channel_id = stg_reactor_timeseries.channel_id
    )
    
    union all
    
    select
        {{ dbt_utils.generate_surrogate_key(['reading_timestamp', 'channel_id', 'issue_type']) }} as issue_id,
        reading_timestamp,
        channel_id,
        reading_value,
        'SUSPECT_QUALITY' as issue_type,
        'Source flagged as SUSPECT' as issue_description,
        _source_file,
        current_timestamp as detected_at
    from {{ ref('stg_reactor_timeseries') }}
    where quality_flag = 'SUSPECT'
)

select * from quality_issues
{% if is_incremental() %}
where detected_at > (select max(detected_at) from {{ this }})
{% endif %}
```

---

## Configuration Files

### dbt_project.yml

```yaml
name: 'neutron_os'
version: '0.1.0'
config-version: 2

profile: 'neutron_os'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  neutron_os:
    staging:
      +materialized: view
      +schema: staging
    silver:
      +materialized: incremental
      +schema: silver
      +tags: ['silver']
    gold:
      +materialized: table
      +schema: gold
      +tags: ['gold']

vars:
  # Quality thresholds
  max_missing_rate: 0.05  # 5% missing data allowed
  dedup_window_hours: 24   # Lookback for deduplication
```

### profiles.yml

```yaml
neutron_os:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: '{{ env_var("NEUTRON_WAREHOUSE") }}/neutron_os.duckdb'
      extensions:
        - iceberg
      settings:
        s3_region: 'us-east-1'
    
    prod:
      type: duckdb
      path: '/data/neutron_os/neutron_os.duckdb'
      threads: 4
```

### packages.yml

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  - package: calogica/dbt_expectations
    version: 0.10.1
```

---

## Seed Data

### channel_reference.csv

```csv
channel_id,channel_name,display_name,measurement_type,unit,min_valid_value,max_valid_value,location,instrument_model,calibration_date
CH001,core_power_kw,Core Power,power,kW,0,1100,Core,Keithley 2700,2025-06-15
CH002,pool_temp_c,Pool Temperature,temperature,degC,15,45,Pool,Omega TC-K,2025-06-15
CH003,fuel_temp_c,Fuel Temperature,temperature,degC,20,600,Core,Omega TC-K,2025-06-15
CH004,neutron_flux,Neutron Flux,flux,n/cm2/s,0,1e16,Core,Reuter-Stokes,2025-06-15
```

---

## Testing

### Schema Tests (_silver.yml)

```yaml
version: 2

models:
  - name: reactor_readings
    description: "Cleaned and validated reactor sensor readings"
    columns:
      - name: reading_id
        description: "Surrogate key (timestamp + channel hash)"
        tests:
          - unique
          - not_null
      
      - name: reading_timestamp
        description: "When the measurement was taken"
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: "'2020-01-01'"
              max_value: "current_date + interval '1 day'"
      
      - name: channel_id
        description: "Sensor channel identifier"
        tests:
          - not_null
          - relationships:
              to: ref('channel_metadata')
              field: channel_id
      
      - name: reading_value
        description: "Measured value"
        tests:
          - not_null
      
      - name: validated_quality
        description: "Quality flag after validation"
        tests:
          - accepted_values:
              values: ['GOOD', 'SUSPECT', 'BAD', 'INVALID', 'MISSING']

  - name: channel_metadata
    description: "Reference data for sensor channels"
    columns:
      - name: channel_id
        tests:
          - unique
          - not_null
```

### Custom Tests

```sql
-- tests/assert_no_duplicates.sql
-- Verify no duplicate timestamp+channel combinations

select
    reading_timestamp,
    channel_id,
    count(*) as cnt
from {{ ref('reactor_readings') }}
group by 1, 2
having count(*) > 1
```

```sql
-- tests/assert_valid_timestamps.sql
-- Verify no future timestamps

select *
from {{ ref('reactor_readings') }}
where reading_timestamp > current_timestamp + interval '1 hour'
```

---

## Macros

### quality_checks.sql

```sql
-- macros/quality_checks.sql

{% macro check_value_in_range(column, channel_id_column, metadata_ref) %}
    case
        when {{ column }} < (
            select min_valid_value 
            from {{ metadata_ref }} 
            where channel_id = {{ channel_id_column }}
        ) then 'BELOW_RANGE'
        when {{ column }} > (
            select max_valid_value 
            from {{ metadata_ref }} 
            where channel_id = {{ channel_id_column }}
        ) then 'ABOVE_RANGE'
        else 'IN_RANGE'
    end
{% endmacro %}


{% macro calculate_missing_rate(timestamp_column, channel_column, expected_interval_seconds) %}
    -- Calculate what % of expected readings are missing
    -- Expected: one reading per expected_interval_seconds
    with bounds as (
        select 
            min({{ timestamp_column }}) as min_ts,
            max({{ timestamp_column }}) as max_ts,
            count(*) as actual_count
        from {{ this }}
    ),
    expected as (
        select 
            datediff('second', min_ts, max_ts) / {{ expected_interval_seconds }} as expected_count
        from bounds
    )
    select 
        1.0 - (actual_count::float / nullif(expected_count, 0)) as missing_rate
    from bounds, expected
{% endmacro %}
```

---

## Success Criteria

| Criterion | Measurement |
|-----------|-------------|
| **Deduplication** | Zero duplicate reading_id values |
| **Data Quality** | <5% of readings flagged as non-GOOD |
| **Completeness** | All Bronze rows appear in Silver (or in quality log) |
| **Performance** | Full refresh <5 minutes for 1M rows |
| **Documentation** | 100% of columns have descriptions |
| **Test Coverage** | All models have schema tests passing |

---

## Usage

```bash
# Install dependencies
cd dbt/neutron_os
dbt deps

# Load seed data
dbt seed

# Run staging models
dbt run --select staging

# Run silver models
dbt run --select silver

# Run all tests
dbt test

# Generate documentation
dbt docs generate
dbt docs serve
```

---

## Follow-Up Components

After Silver models are complete:

1. **[Dagster Orchestration](prompt-dagster-orchestration.md)** - Schedule dbt runs
2. **[Superset Dashboards](prompt-superset-dashboards.md)** - Query Silver/Gold tables
3. **Gold Layer Models** - Aggregated metrics (reactor_hourly_metrics, etc.)

---

*This design prompt is part of the Neutron OS documentation. See [Executive Summary](../neutron-os-executive-summary.md) for project context.*
