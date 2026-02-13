# Data Engineering Zoomcamp - Module 5 Notes

## Part 1: Introduction to Data Platforms and Bruin

### What is a Data Platform?

A **data platform** is an integrated set of technologies and tools that enable organizations to collect, store, process, analyze, and derive insights from data at scale.

**Key Components of Modern Data Platforms:**

```
Data Sources → Ingestion → Storage → Processing → Analytics → Visualization
     ↓            ↓          ↓          ↓           ↓            ↓
  APIs        Airflow    Data Lake   dbt/Spark   SQL/Python   Tableau
  Databases   Fivetran   BigQuery    Bruin       Notebooks    Looker
  Files       Custom     Snowflake   Custom      BI Tools     Streamlit
```

**Evolution of Data Platforms:**
1. **Traditional (ETL-based)**: Informatica, SSIS, Talend
2. **Modern Cloud (ELT-based)**: Fivetran + Snowflake + dbt
3. **Next-Gen (All-in-one)**: Integrated platforms like Bruin

### What is Bruin?

**Bruin** is an open-source data platform that combines data ingestion, transformation, and quality management in a single YAML-based tool.

**Official Definition:**
> Bruin is a command-line tool that allows building reliable data pipelines in SQL, Python, or other languages via a simple YAML interface.

**Core Philosophy:**

```
Bruin's Approach:
├── Configuration as Code (YAML)
├── Multi-language Support (SQL, Python, R)
├── Built-in Quality Checks
├── Metadata-first Design
└── Simple CLI Interface
```

**Why Bruin?**

Traditional approach (multiple tools):
```
Fivetran (Ingestion) + dbt (Transform) + Great Expectations (Quality)
= 3 tools, 3 configs, 3 deployments
```

Bruin approach (unified platform):
```
Bruin (Ingestion + Transform + Quality)
= 1 tool, 1 config (YAML), 1 deployment
```

**Key Features:**

1. **Unified Workflow**:
   - Ingestion via `ingestr` (built-in)
   - Transformations in SQL/Python
   - Quality checks in YAML
   - All orchestrated together

2. **Multi-Platform Support**:
   - BigQuery, Snowflake, Redshift
   - PostgreSQL, DuckDB, MySQL
   - Databricks, Athena, and more

3. **Metadata-Driven**:
   - Column descriptions
   - Data lineage
   - Auto-generated documentation

4. **Quality-First**:
   - Built-in column checks
   - Custom SQL checks
   - Automated testing

---

## Part 2: Bruin Project Structure

### Required Files and Directories

Every Bruin project has a specific structure:

```
my-bruin-project/
├── .bruin.yml              # Environment & connection config (REQUIRED)
├── pipeline.yml            # Pipeline definition (REQUIRED)
└── assets/                 # Asset folder (REQUIRED)
    ├── ingestion/
    │   └── trips.py
    ├── staging/
    │   └── stg_trips.sql
    └── core/
        └── fact_trips.sql
```

**Critical Files:**

1. **`.bruin.yml`** (Environment Configuration)
```yaml
environments:
  default:
    connections:
      google_cloud_platform:
        - name: my-gcp
          service_account_file: /path/to/key.json
          project_id: my-project
```

2. **`pipeline.yml`** (Pipeline Definition)
```yaml
name: taxi_pipeline
schedule: daily
start_date: "2024-01-01"

default_connections:
  google_cloud_platform: "my-gcp"

variables:
  taxi_types:
    type: array
    items:
      type: string
    default: ["yellow", "green"]
```

3. **`assets/`** (Required Directory)
   - Must be present next to `pipeline.yml`
   - Contains all transformation files
   - Organized by layer (ingestion, staging, core, marts)

**Important Notes:**
- Assets CANNOT be placed anywhere - they must be in the `assets/` folder
- The `.bruin.yml` file starts with a dot (hidden file)
- `pipeline.yml` is at the root level, NOT in a `pipeline/` folder

---

## Part 3: Bruin Assets

### What are Assets?

**Assets** are the building blocks of a Bruin pipeline - individual data processing units.

**Asset Types:**

```
Asset Types in Bruin:
├── SQL Assets (.sql)        # SQL transformations
├── Python Assets (.py)      # Python scripts
├── R Assets (.r)            # R scripts
├── Ingestr Assets (.asset.yml) # Data ingestion
└── Sensor Assets            # Dependency monitoring
```

### SQL Assets

SQL assets are the most common - they execute SQL queries to transform data.

**Example: Staging SQL Asset**

```sql
-- assets/staging/stg_trips.sql

/* @bruin

name: staging.trips
type: sql
materialization:
  type: table
  
columns:
  - name: trip_id
    type: string
    description: "Unique identifier for the trip"
    checks:
      - not_null
      - unique
      
  - name: pickup_datetime
    type: timestamp
    description: "When the trip started"
    checks:
      - not_null

depends:
  - ingestion.raw_trips

@bruin */

SELECT
    trip_id,
    CAST(pickup_datetime AS TIMESTAMP) AS pickup_datetime,
    CAST(passenger_count AS INT64) AS passenger_count,
    CAST(total_amount AS NUMERIC) AS total_amount
FROM ingestion.raw_trips
WHERE trip_id IS NOT NULL
```

**Asset Definition Structure:**

```
/* @bruin
[Metadata in YAML format]
@bruin */

[SQL Query]
```

### Python Assets

Python assets allow custom logic, API calls, or complex transformations.

**Example: Ingestion Python Asset**

```python
# assets/ingestion/trips.py

"""
@bruin
name: ingestion.trips
type: python
materialization:
  type: table

depends: []

@bruin
"""

import pandas as pd
from bruin import BruinContext

def main(context: BruinContext):
    # Download data
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
    df = pd.read_parquet(url)
    
    # Return dataframe to be materialized
    return df
```

### Ingestr Assets

Ingestr assets use Bruin's built-in ingestion engine to load data from external sources.

**Example: Ingestr Asset**

```yaml
# assets/ingestion/google_sheets.asset.yml

name: ingestion.sheet_data
type: ingestr

source:
  name: gsheet
  connection: google_sheets
  properties:
    spreadsheet_id: "1abc...xyz"
    sheet_name: "Sales Data"

destination:
  name: bigquery
  connection: my-gcp
  properties:
    dataset: raw
    table: sheet_data
```

---

## Part 4: Materialization Strategies

### What is Materialization?

**Materialization** determines how Bruin creates or updates your data in the warehouse.

**Available Strategies:**

| Strategy | Description | Use Case | Rebuild Behavior |
|----------|-------------|----------|------------------|
| **table** | Creates a physical table | Default, most assets | Full replacement |
| **view** | Creates a virtual view | Lightweight transformations | Always rebuilt |
| **replace** | Truncate & rebuild | Smaller datasets | Full replacement |
| **append** | Add new rows only | Event logs, immutable data | Only new data |
| **time_interval** | Incremental by time column | Time-series data | Incremental updates |

### Time Interval Strategy (Most Important for Large Datasets)

The `time_interval` strategy is designed for incremental processing based on a time column.

**When to Use:**
- Large datasets organized by date/time
- Data that grows over time (trips, orders, events)
- Need for deduplication based on time windows

**Configuration:**

```sql
/* @bruin

name: staging.trips
type: sql
materialization:
  type: time_interval
  time_column: pickup_datetime
  interval: day
  
@bruin */

SELECT *
FROM {{ source('raw', 'trips') }}
WHERE pickup_datetime >= CURRENT_DATE()
```

**How it Works:**

First run:
```sql
-- Loads all historical data
CREATE TABLE staging.trips AS
SELECT * FROM raw.trips
```

Subsequent runs:
```sql
-- Only processes new/updated data
INSERT INTO staging.trips
SELECT * FROM raw.trips
WHERE pickup_datetime > (SELECT MAX(pickup_datetime) FROM staging.trips)
```

**Benefits:**
- ✅ Much faster for large tables
- ✅ Automatic deduplication
- ✅ Handles late-arriving data
- ✅ Reduces warehouse costs

**Comparison: Replace vs Time Interval for Staging**

```
Scenario: NYC Taxi data with 100M rows

Replace Strategy:
- Every run: Delete 100M rows, Insert 100M rows
- Runtime: 30 minutes
- Cost: High (full table scan each time)

Time Interval Strategy:
- First run: Insert 100M rows (30 min)
- Daily runs: Insert ~300K new rows (30 seconds)
- Cost: Low (only process new data)
```

**Best Practice for Staging Layer:**
- Use `time_interval` for large, time-based datasets
- Use `view` for lightweight transformations
- Use `table` for frequently-queried staging models

---

## Part 5: Pipeline Variables

### Defining Variables

Variables allow you to parameterize your pipeline for flexibility.

**In `pipeline.yml`:**

```yaml
name: taxi_pipeline

variables:
  # Array variable
  taxi_types:
    type: array
    items:
      type: string
    default: ["yellow", "green"]
  
  # String variable
  dataset:
    type: string
    default: "production"
  
  # Date variable
  start_date:
    type: string
    default: "2024-01-01"
```

### Using Variables in Assets

**In SQL Assets:**

```sql
/* @bruin
name: core.trips
@bruin */

SELECT *
FROM staging.trips
WHERE service_type IN ({{ var("taxi_types") }})
  AND DATE(pickup_datetime) >= '{{ var("start_date") }}'
```

**In Python Assets:**

```python
def main(context: BruinContext):
    taxi_types = context.vars["taxi_types"]
    start_date = context.vars["start_date"]
    
    df = load_data(taxi_types, start_date)
    return df
```

### Overriding Variables at Runtime

**Command-line Override:**

```bash
# Override single value
bruin run --var start_date=2024-06-01

# Override array (JSON format)
bruin run --var 'taxi_types=["yellow"]'

# Multiple overrides
bruin run --var start_date=2024-06-01 --var 'taxi_types=["green"]'
```

**Why Use Variables?**
- ✅ Test with subset of data
- ✅ Reprocess specific time periods
- ✅ Environment-specific configurations
- ✅ Dynamic pipeline behavior

---

## Part 6: Running Bruin Pipelines

### Basic Commands

**Initialize a new project:**

```bash
bruin init my-pipeline
cd my-pipeline
```

**Validate pipeline:**

```bash
bruin validate
# Checks: YAML syntax, SQL compilation, dependencies
```

**Run entire pipeline:**

```bash
bruin run
```

**Run specific asset:**

```bash
bruin run assets/staging/stg_trips.sql
```

### Running with Dependencies

**Downstream Flag** - Run asset + all assets that depend on it:

```bash
# Correct syntax
bruin run ingestion/trips.py --downstream

# This runs:
# 1. ingestion/trips.py
# 2. staging/stg_trips.sql (depends on ingestion)
# 3. core/fact_trips.sql (depends on staging)
```

**Why Use `--downstream`?**
- You modified an upstream asset
- Need to propagate changes downstream
- Testing data lineage
- Ensuring consistency after changes

**Other Useful Flags:**

```bash
# Run with full refresh (recreate from scratch)
bruin run --full-refresh

# Run only specific layer
bruin run --tag staging

# Dry run (validate without executing)
bruin run --dry-run
```

---

## Part 7: Quality Checks

### Column-Level Checks

Bruin provides built-in quality checks for data validation.

**Available Column Checks:**

```yaml
columns:
  - name: trip_id
    checks:
      - not_null      # No NULL values
      - unique        # All values unique
      
  - name: passenger_count
    checks:
      - positive      # Values > 0
      
  - name: vendor_id
    checks:
      - accepted_values: [1, 2]  # Only these values allowed
```

**Example: Trips Table with Quality Checks**

```sql
/* @bruin

name: core.trips
type: sql

columns:
  - name: trip_id
    type: string
    description: "Unique trip identifier"
    checks:
      - not_null: true
      - unique: true
      
  - name: pickup_datetime
    type: timestamp
    description: "Trip start time"
    checks:
      - not_null: true
      
  - name: total_amount
    type: numeric
    description: "Total trip cost in USD"
    checks:
      - not_null: true
      - positive: true
      
  - name: service_type
    type: string
    checks:
      - accepted_values: ["yellow", "green", "fhv"]

@bruin */

SELECT *
FROM {{ ref('staging.trips') }}
```

**What Happens When Checks Fail?**

```bash
bruin run

# Output:
✓ core.trips - materialization successful
✗ core.trips - quality check failed: column 'total_amount' has NULL values (found 42 rows)
```

### Custom SQL Checks

For complex validation logic:

```sql
/* @bruin

name: core.trips
type: sql

custom_checks:
  - name: reasonable_fare
    query: |
      SELECT COUNT(*) as failures
      FROM {QUALIFIED_NAME}
      WHERE total_amount < 0 OR total_amount > 1000
    
  - name: valid_trip_duration
    query: |
      SELECT COUNT(*) as failures
      FROM {QUALIFIED_NAME}
      WHERE TIMESTAMP_DIFF(dropoff_datetime, pickup_datetime, MINUTE) < 0

@bruin */
```

---

## Part 8: Lineage and Documentation

### Viewing Lineage

**Lineage Graph** shows dependencies between assets.

```bash
# Show lineage for entire pipeline
bruin lineage

# Show lineage for specific asset
bruin lineage assets/core/fact_trips.sql
```

**Example Lineage:**

```
ingestion.raw_yellow_trips
         ↓
  staging.stg_yellow
         ↓              ↘
         ↓                core.dim_zones
         ↓              ↗
    core.fact_trips
         ↓
   marts.monthly_revenue
```

**Why Lineage Matters:**
- ✅ Understand data flow
- ✅ Impact analysis (what breaks if I change this?)
- ✅ Debugging data quality issues
- ✅ Documentation for new team members

### Auto-Generated Documentation

Bruin automatically generates documentation from your asset definitions.

**What Gets Documented:**
- Asset descriptions
- Column names and types
- Column descriptions
- Quality checks
- Dependencies
- Lineage graph

**Accessing Documentation:**

```bash
# Generate documentation
bruin docs generate

# Serve documentation locally
bruin docs serve
# Opens at http://localhost:8080
```

---

## Part 9: First-Time Runs and Full Refresh

### Full Refresh Flag

When running a pipeline for the first time or recreating tables from scratch:

```bash
bruin run --full-refresh
```

**What `--full-refresh` Does:**

1. **Drops existing tables** (if they exist)
2. **Recreates from scratch** (ignoring incremental logic)
3. **Reprocesses all historical data**
4. **Runs all quality checks**

**When to Use:**

- ✅ First-time pipeline run on new database
- ✅ Schema changes that require rebuild
- ✅ Fixing data quality issues in historical data
- ✅ Testing full pipeline from scratch

**Example Scenario:**

```bash
# New DuckDB database, first run
bruin run --full-refresh

# Output:
✓ Dropped table: staging.trips
✓ Created table: staging.trips (1.2M rows)
✓ Dropped table: core.fact_trips  
✓ Created table: core.fact_trips (1.2M rows)
```

**Incremental vs Full Refresh:**

```
Normal Run (Incremental):
- Checks MAX(pickup_datetime) in existing table
- Only processes new data since last run
- Fast, efficient

Full Refresh Run:
- Ignores existing data completely
- Reprocesses everything from source
- Slow, but ensures consistency
```

---

## Part 10: Bruin Best Practices

### Project Organization

**Recommended Structure:**

```
my-pipeline/
├── .bruin.yml
├── pipeline.yml
├── assets/
│   ├── ingestion/           # Raw data ingestion
│   │   ├── source_a/
│   │   └── source_b/
│   ├── staging/             # Clean & standardize
│   │   ├── stg_source_a/
│   │   └── stg_source_b/
│   ├── intermediate/        # Complex joins (optional)
│   │   └── int_joined_data/
│   ├── core/                # Facts & dimensions
│   │   ├── dim_*.sql
│   │   └── fact_*.sql
│   └── marts/               # Business-specific
│       ├── finance/
│       └── marketing/
```

### Layer-Specific Guidance

**Ingestion Layer:**
- Use `ingestr` assets or Python for API calls
- Materialize as `table`
- Minimal transformations
- Land raw data as-is

**Staging Layer:**
- One asset per source table
- Use `time_interval` for large datasets
- Light transformations only (cast, rename, filter)
- Column-level quality checks
- Materialize as `view` or `time_interval`

**Core Layer:**
- Facts and dimensions
- Join staging models
- Apply business logic
- Materialize as `table`
- Comprehensive quality checks

**Marts Layer:**
- Business-specific aggregations
- Pre-calculated metrics for dashboards
- Materialize as `table`

### Naming Conventions

**Files:**
- Staging: `stg_<source>_<entity>.sql`
- Core dimensions: `dim_<entity>.sql`
- Core facts: `fact_<entity>.sql`
- Intermediate: `int_<description>.sql`

**Columns:**
- Use `snake_case`
- Timestamps: `*_datetime` or `*_at`
- Booleans: `is_*` or `has_*`
- IDs: `*_id`

---

## Part 11: Comparison with dbt

### Bruin vs dbt

| Aspect | Bruin | dbt |
|--------|-------|-----|
| **Configuration** | YAML in SQL comments | Separate YAML files |
| **Ingestion** | Built-in (ingestr) | External tool needed |
| **Quality Checks** | Built-in column checks | dbt_expectations package |
| **Materialization** | `time_interval` strategy | Incremental models |
| **Languages** | SQL, Python, R | Primarily SQL |
| **Learning Curve** | Simpler (unified) | Steeper (more concepts) |
| **Ecosystem** | Smaller, growing | Mature, large community |
| **Documentation** | Auto-generated | Auto-generated |
| **Orchestration** | Built-in CLI | External orchestrator |

### When to Use Bruin vs dbt

**Use Bruin when:**
- ✅ Starting a new project from scratch
- ✅ Need unified ingestion + transformation
- ✅ Want simpler configuration
- ✅ Working with smaller teams
- ✅ Using Python/R alongside SQL

**Use dbt when:**
- ✅ Already invested in dbt ecosystem
- ✅ Need extensive community packages
- ✅ Require enterprise dbt Cloud features
- ✅ Pure SQL transformations only
- ✅ Large data team with dbt expertise

### Migration Path

**dbt to Bruin:**

1. **Project Structure**: Similar concepts (staging, core, marts)
2. **Models**: Convert dbt models to Bruin SQL assets
3. **Tests**: Map dbt tests to Bruin column checks
4. **Macros**: Rewrite as Bruin macros or Python functions
5. **Sources**: Convert to Bruin ingestr assets

**Example Conversion:**

dbt model:
```sql
-- models/staging/stg_orders.sql
{{ config(materialized='view') }}

SELECT * FROM {{ source('raw', 'orders') }}
```

Bruin equivalent:
```sql
/* @bruin
name: staging.orders
type: sql
materialization:
  type: view
@bruin */

SELECT * FROM {{ source('raw', 'orders') }}
```

---

## Part 12: Deployment and Production

### Local Development Workflow

```bash
# 1. Make changes to assets
vim assets/staging/stg_trips.sql

# 2. Validate changes
bruin validate

# 3. Test run specific asset
bruin run assets/staging/stg_trips.sql --downstream

# 4. Run full pipeline
bruin run
```

### CI/CD with Bruin

**GitHub Actions Example:**

```yaml
# .github/workflows/bruin-ci.yml
name: Bruin CI

on:
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install Bruin
        run: |
          curl -LsSf https://raw.githubusercontent.com/bruin-data/bruin/main/install.sh | sh
      
      - name: Validate Pipeline
        run: bruin validate
      
      - name: Run Tests
        run: bruin run --dry-run
```

### Scheduling Production Runs

**Option 1: Cron**

```bash
# crontab -e
0 2 * * * cd /path/to/pipeline && bruin run --full-refresh
```

**Option 2: Airflow**

```python
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG('bruin_pipeline', schedule_interval='@daily') as dag:
    run_bruin = BashOperator(
        task_id='run_bruin',
        bash_command='cd /path/to/pipeline && bruin run'
    )
```

**Option 3: Bruin Cloud** (Managed Service)
- Web-based scheduling
- Monitoring and alerting
- Centralized logging
- Team collaboration

---

## Part 13: Key Concepts Summary

### Critical Takeaways

**1. Project Structure:**
- `.bruin.yml` (connections) + `pipeline.yml` (config) + `assets/` (code) are ALL required
- Assets must be in `assets/` folder, not anywhere else

**2. Materialization Strategies:**
- Use `time_interval` for large time-series data in staging
- Use `table` for core facts and dimensions
- Use `view` for lightweight transformations
- Use `replace` for small datasets that need full refresh

**3. Pipeline Variables:**
- Override at runtime with `--var 'name=value'`
- Array variables need JSON syntax: `--var 'types=["a","b"]'`

**4. Running Pipelines:**
- `bruin run` - entire pipeline
- `bruin run path/to/asset.sql` - specific asset
- `bruin run path/to/asset.sql --downstream` - asset + dependents
- `bruin run --full-refresh` - recreate everything from scratch

**5. Quality Checks:**
- `not_null` - no NULL values allowed
- `unique` - all values must be unique
- `positive` - values must be > 0
- `accepted_values` - whitelist of allowed values

**6. Lineage:**
- `bruin lineage` - view dependency graph
- Understand upstream and downstream impacts
- Essential for debugging and documentation

---

## Part 14: Hands-On Example - NYC Taxi Pipeline

### Complete Pipeline Structure

```
nyc-taxi-pipeline/
├── .bruin.yml
├── pipeline.yml
└── assets/
    ├── ingestion/
    │   └── raw_trips.py
    ├── staging/
    │   ├── stg_green_trips.sql
    │   └── stg_yellow_trips.sql
    ├── core/
    │   ├── dim_zones.sql
    │   └── fact_trips.sql
    └── marts/
        └── monthly_revenue.sql
```

### Configuration Files

**`.bruin.yml`:**

```yaml
environments:
  default:
    connections:
      google_cloud_platform:
        - name: my-gcp
          project_id: de-zoomcamp-2025
          dataset: taxi_data
          service_account_file: ./service-account.json
```

**`pipeline.yml`:**

```yaml
name: nyc_taxi_pipeline
schedule: daily
start_date: "2024-01-01"

default_connections:
  google_cloud_platform: "my-gcp"

variables:
  taxi_types:
    type: array
    items:
      type: string
    default: ["yellow", "green"]
  
  year:
    type: string
    default: "2024"
```

### Asset Examples

**Ingestion (Python):**

```python
# assets/ingestion/raw_trips.py

"""
@bruin
name: ingestion.raw_yellow_trips
type: python
materialization:
  type: table
@bruin
"""

import pandas as pd
from bruin import BruinContext

def main(context: BruinContext):
    year = context.vars["year"]
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-01.parquet"
    df = pd.read_parquet(url)
    return df
```

**Staging (SQL with Time Interval):**

```sql
-- assets/staging/stg_yellow_trips.sql

/* @bruin

name: staging.yellow_trips
type: sql
materialization:
  type: time_interval
  time_column: pickup_datetime
  interval: day

columns:
  - name: trip_id
    type: string
    checks:
      - not_null: true
      - unique: true
  
  - name: pickup_datetime
    type: timestamp
    checks:
      - not_null: true

depends:
  - ingestion.raw_yellow_trips

@bruin */

SELECT
    GENERATE_UUID() AS trip_id,
    CAST(tpep_pickup_datetime AS TIMESTAMP) AS pickup_datetime,
    CAST(tpep_dropoff_datetime AS TIMESTAMP) AS dropoff_datetime,
    CAST(passenger_count AS INT64) AS passenger_count,
    CAST(trip_distance AS NUMERIC) AS trip_distance,
    CAST(fare_amount AS NUMERIC) AS fare_amount,
    CAST(total_amount AS NUMERIC) AS total_amount,
    'yellow' AS service_type
FROM {{ ref('ingestion.raw_yellow_trips') }}
WHERE tpep_pickup_datetime IS NOT NULL
```

**Core Fact Table:**

```sql
-- assets/core/fact_trips.sql

/* @bruin

name: core.fact_trips
type: sql
materialization:
  type: table

columns:
  - name: trip_id
    checks:
      - not_null: true
      - unique: true
  
  - name: total_amount
    checks:
      - not_null: true
      - positive: true

depends:
  - staging.yellow_trips
  - staging.green_trips

@bruin */

SELECT * FROM {{ ref('staging.yellow_trips') }}
UNION ALL
SELECT * FROM {{ ref('staging.green_trips') }}
```

### Running the Pipeline

```bash
# 1. Initialize and validate
bruin validate

# 2. First-time full run
bruin run --full-refresh

# 3. Daily incremental runs
bruin run

# 4. Run only yellow taxi data
bruin run --var 'taxi_types=["yellow"]'

# 5. View lineage
bruin lineage

# 6. Generate docs
bruin docs generate
bruin docs serve
```

---

## Additional Resources

### Official Documentation
- **Bruin Documentation**: https://getbruin.com/docs