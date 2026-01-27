# Design Prompt: Bronze Layer Ingestion

**Component:** Data Ingestion Pipeline  
**Phase:** 1 (Foundation)  
**Priority:** P0 - Critical Path  
**Estimated Effort:** 2-3 days

---

## Context for Implementation

This prompt is designed to guide Claude Code (or a developer) through building the Bronze layer ingestion system for Neutron OS. The Bronze layer is the foundation—raw data exactly as received, stored in Apache Iceberg tables for time-travel and schema evolution.

**Pre-requisites:**
- Python 3.11+ environment
- PyIceberg library installed
- Access to sample TRIGA sensor data (CSV files)
- Local filesystem or S3-compatible storage for Iceberg warehouse

---

## Objective

Build a Python module that ingests TRIGA reactor sensor data from CSV files into Apache Iceberg Bronze tables. The ingestion must be:

1. **Idempotent** - Re-running on the same file produces no duplicates
2. **Auditable** - Every record tracks its source file and ingestion timestamp
3. **Schema-evolving** - New columns in source files are handled gracefully
4. **Partitioned** - Data partitioned by date for efficient queries

---

## Input Specification

### Source Data: TRIGA Sensor CSV

Location: `data/raw/triga_sensors/YYYY-MM-DD/reactor_data_YYYYMMDD_HHMMSS.csv`

Sample format:
```csv
timestamp,channel_id,channel_name,value,unit,quality_flag
2026-01-15T10:30:00.123Z,CH001,core_power_kw,245.7,kW,GOOD
2026-01-15T10:30:00.123Z,CH002,pool_temp_c,28.4,degC,GOOD
2026-01-15T10:30:00.123Z,CH003,fuel_temp_c,312.1,degC,GOOD
2026-01-15T10:30:00.123Z,CH004,neutron_flux,1.23e14,n/cm2/s,SUSPECT
```

### Expected Variations
- Timestamps may be ISO 8601 or Unix epoch milliseconds
- New channels may appear without warning
- Quality flags: `GOOD`, `SUSPECT`, `BAD`, `MISSING`
- Files may have 1K-100K rows each
- Multiple files per day, arriving continuously

---

## Output Specification

### Target: Iceberg Bronze Table

Table name: `bronze.reactor_timeseries_raw`

Schema:
```sql
CREATE TABLE bronze.reactor_timeseries_raw (
    -- Business columns (from source)
    event_timestamp     TIMESTAMP WITH TIME ZONE,
    channel_id          STRING,
    channel_name        STRING,
    value               DOUBLE,
    unit                STRING,
    quality_flag        STRING,
    
    -- Audit columns (added by ingestion)
    _source_file        STRING,       -- Full path to source file
    _ingestion_ts       TIMESTAMP,    -- When this record was ingested
    _batch_id           STRING,       -- UUID for this ingestion batch
    _row_hash           STRING        -- SHA256 of business columns for dedup
)
PARTITIONED BY (days(event_timestamp))
```

---

## Implementation Requirements

### 1. Module Structure

```
src/neutron_os/ingestion/
├── __init__.py
├── bronze_ingest.py      # Main ingestion logic
├── schemas.py            # Iceberg schema definitions
├── dedup.py              # Deduplication logic
└── config.py             # Configuration management
```

### 2. Core Functions

```python
# bronze_ingest.py

def ingest_csv_to_bronze(
    csv_path: Path,
    catalog: Catalog,
    table_name: str = "bronze.reactor_timeseries_raw",
    batch_id: str | None = None,
) -> IngestResult:
    """
    Ingest a single CSV file into the Bronze Iceberg table.
    
    Args:
        csv_path: Path to the CSV file
        catalog: PyIceberg catalog instance
        table_name: Fully qualified table name
        batch_id: Optional batch identifier (generated if not provided)
    
    Returns:
        IngestResult with row counts and any errors
    
    Raises:
        SchemaEvolutionError: If new columns require schema update
        DuplicateDataError: If file was already ingested (idempotency check)
    """
    pass


def ingest_directory(
    directory: Path,
    catalog: Catalog,
    pattern: str = "*.csv",
    parallel: bool = True,
) -> list[IngestResult]:
    """
    Ingest all matching files from a directory.
    
    Handles:
    - Recursive directory scanning
    - Parallel ingestion (if enabled)
    - Progress tracking
    - Error aggregation
    """
    pass
```

### 3. Deduplication Strategy

Use content-based hashing for idempotency:

```python
def compute_row_hash(row: dict) -> str:
    """
    Compute SHA256 hash of business columns.
    
    Hash includes: event_timestamp, channel_id, value
    Does NOT include: audit columns, quality_flag (may be corrected)
    """
    content = f"{row['event_timestamp']}|{row['channel_id']}|{row['value']}"
    return hashlib.sha256(content.encode()).hexdigest()


def check_file_already_ingested(catalog: Catalog, source_file: str) -> bool:
    """
    Check if this source file was already ingested.
    
    Query: SELECT COUNT(*) FROM bronze.reactor_timeseries_raw 
           WHERE _source_file = ?
    """
    pass
```

### 4. Schema Evolution Handling

```python
def handle_schema_evolution(
    current_schema: Schema,
    incoming_columns: list[str],
    catalog: Catalog,
    table_name: str,
) -> Schema:
    """
    Detect new columns in source data and evolve Iceberg schema.
    
    Rules:
    - New columns added as nullable STRING type
    - Column removal: keep in schema, values become NULL
    - Type changes: raise error (manual intervention required)
    
    Returns updated schema.
    """
    pass
```

### 5. Configuration

```python
# config.py

from pydantic import BaseSettings

class IngestionConfig(BaseSettings):
    iceberg_catalog_uri: str = "sqlite:///iceberg_catalog.db"
    iceberg_warehouse: str = "./warehouse"
    bronze_table: str = "bronze.reactor_timeseries_raw"
    
    # Behavior
    fail_on_duplicate: bool = False  # Skip duplicates silently
    parallel_workers: int = 4
    batch_size: int = 10000  # Rows per Iceberg append
    
    class Config:
        env_prefix = "NEUTRON_"
```

---

## Testing Requirements

### Unit Tests

```python
# tests/test_bronze_ingest.py

def test_ingest_single_csv():
    """Verify basic CSV ingestion creates correct Iceberg records."""
    pass

def test_idempotency():
    """Verify re-ingesting same file produces no duplicates."""
    pass

def test_schema_evolution():
    """Verify new columns are added to schema automatically."""
    pass

def test_malformed_csv_handling():
    """Verify graceful handling of bad rows."""
    pass

def test_partition_creation():
    """Verify data is partitioned by date correctly."""
    pass
```

### Integration Test

```python
def test_full_pipeline():
    """
    End-to-end test:
    1. Create sample CSV files
    2. Ingest to Bronze
    3. Query with DuckDB
    4. Verify row counts and content
    """
    pass
```

---

## Success Criteria

| Criterion | Measurement |
|-----------|-------------|
| **Correctness** | All source rows appear in Bronze with matching values |
| **Idempotency** | Re-running same ingestion produces identical table state |
| **Performance** | 100K rows ingested in <30 seconds |
| **Auditability** | Every row traceable to source file |
| **Testability** | >90% code coverage, all edge cases covered |

---

## Example Usage

```python
from neutron_os.ingestion import ingest_csv_to_bronze, IngestionConfig
from pyiceberg.catalog import load_catalog

# Initialize
config = IngestionConfig()
catalog = load_catalog("default", **{
    "uri": config.iceberg_catalog_uri,
    "warehouse": config.iceberg_warehouse,
})

# Ingest a single file
result = ingest_csv_to_bronze(
    csv_path=Path("data/raw/triga_sensors/2026-01-15/reactor_data_20260115_103000.csv"),
    catalog=catalog,
)

print(f"Ingested {result.rows_written} rows, {result.rows_skipped} duplicates")

# Ingest a directory
results = ingest_directory(
    directory=Path("data/raw/triga_sensors/2026-01-15/"),
    catalog=catalog,
    pattern="*.csv",
)

total_rows = sum(r.rows_written for r in results)
print(f"Batch complete: {total_rows} total rows across {len(results)} files")
```

---

## Dependencies

```toml
# pyproject.toml (relevant section)

[project]
dependencies = [
    "pyiceberg>=0.6.0",
    "pyarrow>=14.0.0",
    "pandas>=2.0.0",
    "pydantic>=2.0.0",
    "duckdb>=0.10.0",  # For integration tests
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
]
```

---

## Follow-Up Components

After Bronze ingestion is complete, the next components are:

1. **[dbt Silver Models](prompt-dbt-silver-models.md)** - Transform raw data to cleaned/validated
2. **[Dagster Orchestration](prompt-dagster-orchestration.md)** - Schedule and monitor ingestion
3. **[Superset Dashboards](prompt-superset-dashboards.md)** - Visualize ingested data

---

## Notes for Implementation

- Start with a single-file ingestion function, then generalize
- Use PyArrow for efficient CSV parsing and Iceberg writes
- Consider using `polars` instead of `pandas` for better performance
- The `_row_hash` enables downstream deduplication even if ingestion runs multiple times
- Partition pruning is critical for query performance—verify partitions are created correctly

---

*This design prompt is part of the Neutron OS documentation. See [Executive Summary](../neutron-os-executive-summary.md) for project context.*
