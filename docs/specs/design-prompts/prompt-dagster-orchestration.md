# Design Prompt: Dagster Pipeline Orchestration

**Component:** Workflow Orchestration Layer  
**Phase:** 2 (Core Analytics)  
**Priority:** P1 - High  
**Estimated Effort:** 3-4 days  
**Depends On:** [Bronze Ingestion](prompt-bronze-layer-ingest.md), [dbt Silver Models](prompt-dbt-silver-models.md)

---

## Context for Implementation

This prompt guides building the Dagster orchestration layer that ties together ingestion, transformation, and validation into an observable, schedulable pipeline.

**Why Dagster over Airflow?**
- **Software-defined assets**: Define what data should exist, not just tasks
- **Materialization tracking**: Know when each asset was last updated
- **Native dbt integration**: First-class support via dagster-dbt
- **Local development**: Full UI runs locally without Docker
- **Type system**: Stronger guarantees about data flow

**Pre-requisites:**
- Bronze ingestion module working
- dbt project with Silver models
- Dagster + dagster-dbt installed

---

## Objective

Build a Dagster project that orchestrates the complete Neutron OS data pipeline:

1. **Sensor Ingestion** - Poll for new CSV files, ingest to Bronze
2. **dbt Transforms** - Run staging → Silver → Gold models
3. **Data Quality** - Run dbt tests, track metrics
4. **Alerting** - Notify on failures or quality issues

The pipeline should be:
- **Observable** - Full lineage in Dagster UI
- **Scheduled** - Runs automatically (hourly for sensors, daily for aggregates)
- **Idempotent** - Re-runs produce consistent results
- **Testable** - Unit tests for each asset

---

## Project Structure

```
orchestration/
├── pyproject.toml
├── setup.py
│
├── neutron_os_orchestration/
│   ├── __init__.py
│   ├── definitions.py          # Main Dagster Definitions
│   │
│   ├── assets/
│   │   ├── __init__.py
│   │   ├── bronze_assets.py    # Ingestion assets
│   │   ├── dbt_assets.py       # dbt model assets
│   │   └── quality_assets.py   # Data quality checks
│   │
│   ├── resources/
│   │   ├── __init__.py
│   │   ├── iceberg.py          # Iceberg catalog resource
│   │   └── dbt.py              # dbt CLI resource
│   │
│   ├── jobs/
│   │   ├── __init__.py
│   │   ├── sensor_pipeline.py  # Hourly sensor ingest
│   │   └── daily_refresh.py    # Full daily rebuild
│   │
│   ├── schedules/
│   │   ├── __init__.py
│   │   └── schedules.py        # Cron schedules
│   │
│   └── sensors/
│       ├── __init__.py
│       └── file_sensors.py     # Watch for new CSV files
│
└── tests/
    ├── test_bronze_assets.py
    └── test_dbt_assets.py
```

---

## Asset Definitions

### 1. Bronze Ingestion Assets

```python
# neutron_os_orchestration/assets/bronze_assets.py

from dagster import (
    asset,
    AssetExecutionContext,
    MetadataValue,
    Output,
    DailyPartitionsDefinition,
)
from neutron_os.ingestion import ingest_directory, IngestResult
from pathlib import Path

# Partition by date for incremental processing
daily_partitions = DailyPartitionsDefinition(start_date="2024-01-01")


@asset(
    partitions_def=daily_partitions,
    group_name="bronze",
    description="Raw reactor sensor readings ingested from CSV files",
    compute_kind="python",
)
def bronze_reactor_timeseries(
    context: AssetExecutionContext,
    iceberg_catalog: IcebergCatalogResource,
) -> Output[int]:
    """
    Ingest reactor sensor CSV files for a given date partition.
    
    Watches: data/raw/triga_sensors/{partition_date}/
    Writes to: bronze.reactor_timeseries_raw
    """
    partition_date = context.partition_key
    source_dir = Path(f"data/raw/triga_sensors/{partition_date}")
    
    if not source_dir.exists():
        context.log.info(f"No data directory for {partition_date}")
        return Output(
            value=0,
            metadata={
                "partition_date": partition_date,
                "files_processed": 0,
                "rows_ingested": 0,
            }
        )
    
    # Run ingestion
    catalog = iceberg_catalog.get_catalog()
    results: list[IngestResult] = ingest_directory(
        directory=source_dir,
        catalog=catalog,
        pattern="*.csv",
    )
    
    total_rows = sum(r.rows_written for r in results)
    total_files = len(results)
    
    context.log.info(f"Ingested {total_rows} rows from {total_files} files")
    
    return Output(
        value=total_rows,
        metadata={
            "partition_date": partition_date,
            "files_processed": MetadataValue.int(total_files),
            "rows_ingested": MetadataValue.int(total_rows),
            "source_directory": str(source_dir),
        }
    )


@asset(
    group_name="bronze",
    description="Simulation outputs ingested from HDF5 files",
    compute_kind="python",
)
def bronze_simulation_outputs(
    context: AssetExecutionContext,
    iceberg_catalog: IcebergCatalogResource,
) -> Output[int]:
    """
    Ingest MPACT/SAM simulation outputs.
    
    Watches: data/raw/simulations/
    Writes to: bronze.simulation_outputs_raw
    """
    # Implementation similar to sensor ingestion
    # but with HDF5 parsing logic
    pass
```

### 2. dbt Assets

```python
# neutron_os_orchestration/assets/dbt_assets.py

from dagster import AssetExecutionContext
from dagster_dbt import (
    DbtCliResource,
    dbt_assets,
    DagsterDbtTranslator,
    DagsterDbtTranslatorSettings,
)
from pathlib import Path

# Path to dbt project
DBT_PROJECT_DIR = Path(__file__).parent.parent.parent.parent / "dbt" / "neutron_os"
DBT_MANIFEST_PATH = DBT_PROJECT_DIR / "target" / "manifest.json"


class NeutronDbtTranslator(DagsterDbtTranslator):
    """Custom translator for Neutron OS dbt assets."""
    
    def __init__(self):
        super().__init__(
            settings=DagsterDbtTranslatorSettings(
                enable_asset_checks=True,
            )
        )
    
    def get_group_name(self, dbt_resource_props: dict) -> str:
        """Map dbt schema to Dagster group."""
        schema = dbt_resource_props.get("schema", "")
        if "staging" in schema:
            return "staging"
        elif "silver" in schema:
            return "silver"
        elif "gold" in schema:
            return "gold"
        return "dbt"


@dbt_assets(
    manifest=DBT_MANIFEST_PATH,
    dagster_dbt_translator=NeutronDbtTranslator(),
)
def neutron_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    """
    All dbt models as Dagster assets.
    
    Dagster automatically:
    - Creates assets for each dbt model
    - Infers dependencies from dbt refs
    - Runs dbt tests as asset checks
    """
    yield from dbt.cli(["build"], context=context).stream()
```

### 3. Data Quality Assets

```python
# neutron_os_orchestration/assets/quality_assets.py

from dagster import (
    asset,
    AssetExecutionContext,
    MetadataValue,
    Output,
    AssetCheckResult,
    asset_check,
)
import duckdb


@asset(
    deps=["reactor_readings"],  # Depends on Silver model
    group_name="quality",
    description="Data quality metrics for reactor readings",
    compute_kind="duckdb",
)
def reactor_data_quality_metrics(
    context: AssetExecutionContext,
    duckdb_resource: DuckDBResource,
) -> Output[dict]:
    """
    Compute data quality metrics for the reactor_readings table.
    
    Metrics:
    - Total row count
    - Missing value rates by channel
    - Quality flag distribution
    - Anomaly counts
    """
    conn = duckdb_resource.get_connection()
    
    # Total counts
    total_rows = conn.execute(
        "SELECT COUNT(*) FROM silver.reactor_readings"
    ).fetchone()[0]
    
    # Quality distribution
    quality_dist = conn.execute("""
        SELECT validated_quality, COUNT(*) as cnt
        FROM silver.reactor_readings
        GROUP BY validated_quality
    """).fetchall()
    
    # Missing rate by channel
    missing_rates = conn.execute("""
        SELECT 
            channel_id,
            SUM(CASE WHEN reading_value IS NULL THEN 1 ELSE 0 END)::FLOAT / COUNT(*) as missing_rate
        FROM silver.reactor_readings
        GROUP BY channel_id
    """).fetchall()
    
    metrics = {
        "total_rows": total_rows,
        "quality_distribution": dict(quality_dist),
        "missing_rates": dict(missing_rates),
    }
    
    context.log.info(f"Quality metrics: {metrics}")
    
    return Output(
        value=metrics,
        metadata={
            "total_rows": MetadataValue.int(total_rows),
            "good_rate": MetadataValue.float(
                quality_dist.get("GOOD", 0) / total_rows if total_rows > 0 else 0
            ),
        }
    )


@asset_check(asset=bronze_reactor_timeseries)
def check_no_future_timestamps(
    context: AssetExecutionContext,
    duckdb_resource: DuckDBResource,
) -> AssetCheckResult:
    """Verify no readings have future timestamps."""
    conn = duckdb_resource.get_connection()
    
    future_count = conn.execute("""
        SELECT COUNT(*) 
        FROM bronze.reactor_timeseries_raw
        WHERE event_timestamp > CURRENT_TIMESTAMP + INTERVAL '1 hour'
    """).fetchone()[0]
    
    return AssetCheckResult(
        passed=future_count == 0,
        metadata={"future_timestamp_count": future_count},
    )
```

---

## Resources

### Iceberg Catalog Resource

```python
# neutron_os_orchestration/resources/iceberg.py

from dagster import ConfigurableResource, InitResourceContext
from pyiceberg.catalog import load_catalog
from pydantic import Field


class IcebergCatalogResource(ConfigurableResource):
    """Resource for accessing the Iceberg catalog."""
    
    catalog_name: str = Field(default="default")
    catalog_uri: str = Field(default="sqlite:///iceberg_catalog.db")
    warehouse_path: str = Field(default="./warehouse")
    
    def get_catalog(self):
        return load_catalog(
            self.catalog_name,
            **{
                "uri": self.catalog_uri,
                "warehouse": self.warehouse_path,
            }
        )
```

### DuckDB Resource

```python
# neutron_os_orchestration/resources/duckdb.py

from dagster import ConfigurableResource
import duckdb
from pydantic import Field


class DuckDBResource(ConfigurableResource):
    """Resource for DuckDB connections."""
    
    database_path: str = Field(default="./warehouse/neutron_os.duckdb")
    
    def get_connection(self) -> duckdb.DuckDBPyConnection:
        conn = duckdb.connect(self.database_path)
        # Load Iceberg extension
        conn.execute("INSTALL iceberg; LOAD iceberg;")
        return conn
```

---

## Jobs and Schedules

### Sensor Pipeline Job

```python
# neutron_os_orchestration/jobs/sensor_pipeline.py

from dagster import define_asset_job, AssetSelection

# Job that runs sensor ingestion + dbt transforms
sensor_pipeline_job = define_asset_job(
    name="sensor_pipeline",
    selection=AssetSelection.groups("bronze", "staging", "silver"),
    description="Ingest new sensor data and refresh Silver models",
    tags={"pipeline": "sensor"},
)
```

### Schedules

```python
# neutron_os_orchestration/schedules/schedules.py

from dagster import (
    ScheduleDefinition,
    build_schedule_from_partitioned_job,
    DefaultScheduleStatus,
)
from ..jobs.sensor_pipeline import sensor_pipeline_job

# Run sensor pipeline hourly
hourly_sensor_schedule = ScheduleDefinition(
    job=sensor_pipeline_job,
    cron_schedule="0 * * * *",  # Every hour
    default_status=DefaultScheduleStatus.RUNNING,
)

# Daily full refresh
daily_refresh_schedule = ScheduleDefinition(
    name="daily_full_refresh",
    job=sensor_pipeline_job,
    cron_schedule="0 2 * * *",  # 2 AM daily
    default_status=DefaultScheduleStatus.RUNNING,
)
```

### File Sensor

```python
# neutron_os_orchestration/sensors/file_sensors.py

from dagster import (
    sensor,
    RunRequest,
    SensorEvaluationContext,
    SkipReason,
)
from pathlib import Path
import os

WATCH_DIR = Path("data/raw/triga_sensors")


@sensor(
    job=sensor_pipeline_job,
    minimum_interval_seconds=60,  # Check every minute
)
def new_csv_file_sensor(context: SensorEvaluationContext):
    """
    Watch for new CSV files and trigger ingestion.
    
    Uses cursor to track last processed file.
    """
    last_mtime = float(context.cursor) if context.cursor else 0
    
    # Find newest file
    newest_mtime = last_mtime
    new_files = []
    
    for csv_file in WATCH_DIR.rglob("*.csv"):
        mtime = csv_file.stat().st_mtime
        if mtime > last_mtime:
            new_files.append(csv_file)
            newest_mtime = max(newest_mtime, mtime)
    
    if new_files:
        context.log.info(f"Found {len(new_files)} new CSV files")
        
        # Update cursor
        context.update_cursor(str(newest_mtime))
        
        # Trigger run
        yield RunRequest(
            run_key=f"csv-ingest-{newest_mtime}",
            tags={"trigger": "file_sensor", "file_count": str(len(new_files))},
        )
    else:
        yield SkipReason("No new CSV files found")
```

---

## Main Definitions

```python
# neutron_os_orchestration/definitions.py

from dagster import Definitions, load_assets_from_modules
from dagster_dbt import DbtCliResource

from . import assets
from .resources.iceberg import IcebergCatalogResource
from .resources.duckdb import DuckDBResource
from .jobs.sensor_pipeline import sensor_pipeline_job
from .schedules.schedules import hourly_sensor_schedule, daily_refresh_schedule
from .sensors.file_sensors import new_csv_file_sensor

# Load all assets
all_assets = load_assets_from_modules([assets])

# Define resources
resources = {
    "iceberg_catalog": IcebergCatalogResource(
        catalog_uri="sqlite:///iceberg_catalog.db",
        warehouse_path="./warehouse",
    ),
    "duckdb_resource": DuckDBResource(
        database_path="./warehouse/neutron_os.duckdb",
    ),
    "dbt": DbtCliResource(
        project_dir="./dbt/neutron_os",
    ),
}

# Main Dagster Definitions
defs = Definitions(
    assets=all_assets,
    resources=resources,
    jobs=[sensor_pipeline_job],
    schedules=[hourly_sensor_schedule, daily_refresh_schedule],
    sensors=[new_csv_file_sensor],
)
```

---

## Testing

```python
# tests/test_bronze_assets.py

from dagster import materialize
from neutron_os_orchestration.assets.bronze_assets import bronze_reactor_timeseries
from neutron_os_orchestration.resources.iceberg import IcebergCatalogResource
import tempfile
from pathlib import Path


def test_bronze_ingestion():
    """Test Bronze asset materialization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test CSV
        csv_dir = Path(tmpdir) / "data/raw/triga_sensors/2026-01-15"
        csv_dir.mkdir(parents=True)
        (csv_dir / "test.csv").write_text(
            "timestamp,channel_id,channel_name,value,unit,quality_flag\n"
            "2026-01-15T10:00:00Z,CH001,power,100.0,kW,GOOD\n"
        )
        
        # Materialize
        result = materialize(
            [bronze_reactor_timeseries],
            resources={
                "iceberg_catalog": IcebergCatalogResource(
                    catalog_uri=f"sqlite:///{tmpdir}/catalog.db",
                    warehouse_path=tmpdir,
                ),
            },
            partition_key="2026-01-15",
        )
        
        assert result.success
        assert result.output_for_node("bronze_reactor_timeseries") == 1
```

---

## Success Criteria

| Criterion | Measurement |
|-----------|-------------|
| **Asset Graph** | Complete lineage visible in Dagster UI |
| **Scheduling** | Hourly runs complete within 10 minutes |
| **Sensor Response** | New files detected within 2 minutes |
| **Error Handling** | Failures logged with clear messages |
| **Observability** | All assets have metadata attached |
| **Testability** | All assets have unit tests |

---

## Usage

```bash
# Install
pip install -e ".[dev]"

# Generate dbt manifest (required for dbt assets)
cd dbt/neutron_os && dbt parse && cd ../..

# Run Dagster dev server
dagster dev -m neutron_os_orchestration.definitions

# Materialize assets manually
dagster asset materialize --select bronze_reactor_timeseries --partition 2026-01-15

# Run a job
dagster job execute -j sensor_pipeline
```

---

## Follow-Up Components

After Dagster orchestration is complete:

1. **[Superset Dashboards](prompt-superset-dashboards.md)** - Visualize pipeline outputs
2. **Alerting Integration** - Slack/email on failures
3. **Streaming Upgrade** - Replace file sensor with Kafka/Redpanda

---

*This design prompt is part of the Neutron OS documentation. See [Executive Summary](../neutron-os-executive-summary.md) for project context.*
