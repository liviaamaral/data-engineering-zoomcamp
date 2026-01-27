# Data Engineering Zoomcamp - Module 2 Notes

## Module Overview: Workflow Orchestration with Kestra

Module 2 focuses on workflow orchestration using Kestra, an open-source orchestration platform. You'll learn how to automate and manage complex data pipelines, moving beyond manual ETL processes to build production-ready, scheduled workflows.

---

## Part 1: Introduction to Workflow Orchestration

### What is Workflow Orchestration?

Workflow orchestration is the process of organizing, managing, and automating complex workflows where multiple tasks or processes are coordinated to achieve a specific outcome. Think of it like a musical orchestra: different instruments must come in at the right time under the conductor's direction to create harmonious music. Similarly, in data pipelines, multiple scripts and tasks must work together seamlessly.

**Orchestration vs. Automation:**
- **Automation**: Executing individual tasks without human intervention
- **Orchestration**: Coordinating multiple automated tasks to ensure they happen in the right order and under the correct conditions

**Why Orchestration Matters:**
- Ensures tasks execute in the correct sequence
- Handles dependencies between tasks
- Provides visibility into pipeline execution
- Manages error handling and retries
- Enables scheduling and backfilling
- Makes workflows reproducible and maintainable

---

## Part 2: What is Kestra?

### Overview

Kestra is an open-source, event-driven orchestration platform that simplifies building both scheduled and event-driven workflows. It adopts Infrastructure as Code practices for data and process orchestration, enabling you to build reliable workflows with just a few lines of YAML.

**Key Features:**
- **Flexible Development**: No-code, low-code, and full-code (YAML) approaches
- **1000+ Plugins**: Integrations with databases, cloud services, APIs, and more
- **Visual Interface**: Topology view (DAG visualization) and Gantt chart for execution tracking
- **Easy Monitoring**: Built-in log inspection, execution history, and dashboards
- **Scalable**: Infinitely scalable for handling large workloads
- **Event-Driven**: Support for both scheduled and real-time event triggers

### Why Kestra?

- User-friendly UI with drag-and-drop capabilities
- Version control integration (Git sync)
- CI/CD support for production deployments
- Strong community and documentation
- Free and open-source

---

## Part 3: Core Kestra Concepts

### Flow

A **Flow** is the container for your workflow. It defines all the tasks, their order, inputs, outputs, and triggers.

**Flow Structure:**
```yaml
id: my-flow
namespace: company.team
description: "My workflow description"

inputs:
  - id: my_input
    type: STRING
    required: true

variables:
  var1: "value1"

tasks:
  - id: task1
    type: io.kestra.plugin.core.log.Log
    message: "Hello World"

triggers:
  - id: schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 * * *"
```

### Namespace

Namespaces are logical groupings of flows, similar to folders. They help organize workflows by projects, teams, or environments (e.g., `zoomcamp`, `company.team`, `production.etl`).

### Tasks

**Tasks** are the building blocks of flows. They perform specific operations like downloading data, running scripts, querying databases, or uploading files.

**Two Types of Tasks:**
1. **Runnable Tasks**: Perform actual work (API calls, database queries, file operations). Executed by workers.
2. **Flowable Tasks**: Control orchestration logic (branching, looping, parallelization). Executed by the executor.

**Common Task Types:**
- `io.kestra.plugin.core.http.Download`: Download files from URLs
- `io.kestra.plugin.scripts.python.Script`: Execute Python code
- `io.kestra.plugin.scripts.shell.Commands`: Run shell commands
- `io.kestra.plugin.jdbc.postgresql.Query`: Execute SQL queries
- `io.kestra.plugin.gcp.gcs.Upload`: Upload to Google Cloud Storage
- `io.kestra.plugin.gcp.bigquery.Query`: Query BigQuery

### Inputs

**Inputs** are parameters that make flows dynamic. They allow you to pass values at runtime.

**Input Types:**
- `STRING`: Text values
- `INT`: Integers
- `FLOAT`: Decimal numbers
- `DATETIME`: Date and time values
- `BOOLEAN`: True/false values
- `ARRAY`: Lists of values
- `FILE`: File uploads
- `SELECT`: Dropdown options
- `MULTISELECT`: Multiple selection options

**Example:**
```yaml
inputs:
  - id: taxi
    type: SELECT
    values:
      - yellow
      - green
    defaults: yellow
  - id: year
    type: INT
    defaults: 2020
  - id: month
    type: INT
    defaults: 1
```

**Accessing Inputs:**
Use `{{ inputs.input_name }}` syntax to reference inputs in tasks.

### Outputs

**Outputs** are results produced by tasks. They can be reused in later tasks or downloaded if stored in internal storage.

**Accessing Outputs:**
Use `{{ outputs.task_id.output_property }}` to reference outputs from previous tasks.

**Example:**
```yaml
tasks:
  - id: extract
    type: io.kestra.plugin.core.http.Download
    uri: "https://example.com/data.csv"
  
  - id: transform
    type: io.kestra.plugin.scripts.python.Script
    inputFiles:
      data.csv: "{{ outputs.extract.uri }}"
```

### Variables

**Variables** are key-value pairs defined at the flow level for reuse throughout the workflow. They help avoid repetition and make flows more maintainable.

**Example:**
```yaml
variables:
  file: "{{ inputs.taxi }}_tripdata_{{ inputs.year }}-{{ inputs.month }}.csv"
  staging_table: "public.{{ inputs.taxi }}_tripdata_staging"
  table: "public.{{ inputs.taxi }}_tripdata"
```

**Accessing Variables:**
Use `{{ vars.variable_name }}` or `{{ render(vars.variable_name) }}` for dynamic rendering.

### Triggers

**Triggers** automatically start flow execution based on events or schedules.

**Common Trigger Types:**
- **Schedule Trigger**: Run flows on a cron schedule
- **Flow Trigger**: Start a flow when another flow completes
- **Webhook Trigger**: Trigger from HTTP requests
- **File Trigger**: Start when files are created/modified

**Schedule Example:**
```yaml
triggers:
  - id: daily_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 * * *"  # Daily at 9 AM UTC
```

**Cron Syntax:**
```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday=0)
│ │ │ │ │
* * * * *
```

**Common Cron Patterns:**
- `0 9 * * *` - Daily at 9 AM
- `0 */6 * * *` - Every 6 hours
- `0 9 * * 1-5` - Weekdays at 9 AM
- `0 0 1 * *` - First day of every month at midnight

### Plugin Defaults

Plugin Defaults allow you to set default values for task types, avoiding repetition when multiple tasks use the same configuration.

**Example:**
```yaml
pluginDefaults:
  - type: io.kestra.plugin.jdbc.postgresql
    values:
      url: jdbc:postgresql://postgres:5432/ny_taxi
      username: root
      password: root
```

Now all PostgreSQL tasks inherit these connection settings automatically.

---

## Part 4: Setting Up Kestra with Docker Compose

### Docker Compose Configuration

Kestra runs best with Docker Compose. The setup includes:
- Kestra server
- PostgreSQL database (for Kestra's metadata)
- PostgreSQL database (for exercises - same as Module 1)
- pgAdmin (for database management)

**Basic docker-compose.yml:**
```yaml
services:
  kestra:
    image: kestra/kestra:latest
    ports:
      - "8080:8080"
    environment:
      KESTRA_CONFIGURATION: |
        datasources:
          postgres:
            url: jdbc:postgresql://postgres-kestra:5432/kestra
            username: kestra
            password: k3str4
    depends_on:
      - postgres-kestra

  postgres-kestra:
    image: postgres:latest
    environment:
      POSTGRES_DB: kestra
      POSTGRES_USER: kestra
      POSTGRES_PASSWORD: k3str4
    volumes:
      - kestra_postgres_data:/var/lib/postgresql/data

  postgres_zoomcamp:
    image: postgres:latest
    environment:
      POSTGRES_DB: ny_taxi
      POSTGRES_USER: root
      POSTGRES_PASSWORD: root
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: root
    ports:
      - "8081:80"

volumes:
  kestra_postgres_data:
  postgres_data:
```

### Starting Kestra

```bash
# Navigate to the directory with docker-compose.yml
cd 02-workflow-orchestration/

# Start all services
docker compose up -d

# Check running services
docker compose ps

# View logs
docker compose logs -f kestra

# Stop all services
docker compose down
```

### Accessing Kestra

Open your browser and navigate to: `http://localhost:8080`

The Kestra UI provides:
- **Flows**: Create and manage workflows
- **Executions**: View execution history and logs
- **Topology**: Visual DAG representation
- **Gantt**: Timeline view of task execution
- **Logs**: Detailed execution logs
- **Namespace Files**: Manage files used in workflows
- **KV Store**: Key-Value storage for configuration

---

## Part 5: Building Your First ETL Pipeline

### Project 1: Getting Started with a Simple Pipeline

This introductory flow demonstrates extracting data via HTTP REST API, transforming it in Python, and querying it with DuckDB.

**Flow Structure:**
```yaml
id: 01_getting_started_data_pipeline
namespace: zoomcamp

inputs:
  - id: columns_to_keep
    type: ARRAY
    itemType: STRING
    defaults:
      - brand
      - price

tasks:
  - id: extract
    type: io.kestra.plugin.core.http.Download
    uri: https://dummyjson.com/products

  - id: transform
    type: io.kestra.plugin.scripts.python.Script
    containerImage: python:3.11-alpine
    inputFiles:
      data.json: "{{ outputs.extract.uri }}"
    outputFiles:
      - "*.json"
    env:
      COLUMNS_TO_KEEP: "{{ inputs.columns_to_keep }}"
    script: |
      import json
      import os
      
      columns_to_keep_str = os.getenv("COLUMNS_TO_KEEP")
      columns_to_keep = json.loads(columns_to_keep_str)
      
      with open("data.json", "r") as file:
          data = json.load(file)
      
      filtered_data = [
          {column: product.get(column, "N/A") for column in columns_to_keep}
          for product in data["products"]
      ]
      
      with open("products.json", "w") as file:
          json.dump(filtered_data, file, indent=4)

  - id: query
    type: io.kestra.plugin.jdbc.duckdb.Query
    inputFiles:
      products.json: "{{ outputs.transform.outputFiles['products.json'] }}"
    sql: |
      SELECT * FROM read_json_auto('{{ workingDir }}/products.json')
```

**Key Concepts:**
- **Extract**: Downloads JSON data from an API
- **Transform**: Filters data using Python
- **Query**: Analyzes data with DuckDB SQL
- **inputFiles**: Makes files available to tasks
- **outputFiles**: Captures files produced by tasks

---

## Part 6: NYC Taxi Pipeline - Local PostgreSQL

### Project 2: ETL Pipeline with PostgreSQL

This project builds a complete ETL pipeline to load NYC Taxi data into a local PostgreSQL database.

**Dataset:** NYC Yellow and Green Taxi Trip Records (2019-2020)
- Source: NYC Taxi & Limousine Commission (TLC)
- Format: Compressed CSV files (.csv.gz)
- Partitioned by: Taxi type (yellow/green), year, month

**Pipeline Architecture:**
```
Extract → Transform → Load → Cleanup
   ↓         ↓         ↓        ↓
Download  Create    Merge    Truncate
CSV.gz    Staging   to Main  Staging &
          Table     Table    Delete Files
```

### Flow Configuration

**Inputs:**
```yaml
inputs:
  - id: taxi
    type: SELECT
    values:
      - yellow
      - green
    defaults: yellow
  - id: year
    type: INT
    defaults: 2020
  - id: month
    type: INT
    defaults: 1
```

**Variables:**
```yaml
variables:
  file: "{{ inputs.taxi }}_tripdata_{{ inputs.year }}-{{ inputs.month }}.csv"
  staging_table: "public.{{ inputs.taxi }}_tripdata_staging"
  table: "public.{{ inputs.taxi }}_tripdata"
  data: "{{ outputs.extract.outputFiles[inputs.taxi ~ '_tripdata_' ~ inputs.year ~ '-' ~ inputs.month ~ '.csv'] }}"
```

**Plugin Defaults (PostgreSQL Connection):**
```yaml
pluginDefaults:
  - type: io.kestra.plugin.jdbc.postgresql
    values:
      url: jdbc:postgresql://postgres_zoomcamp:5432/ny_taxi
      username: root
      password: root
```

### Task 1: Extract Data

Downloads and unzips the CSV file from GitHub.

```yaml
- id: extract
  type: io.kestra.plugin.scripts.shell.Commands
  outputFiles:
    - "*.csv"
  taskRunner:
    type: io.kestra.plugin.core.runner.Process
  commands:
    - wget -qO- https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{{ inputs.taxi }}/{{ render(vars.file) }}.gz | gunzip > {{ render(vars.file) }}
```

**Explanation:**
- `wget -qO-`: Download file quietly, output to stdout
- `gunzip`: Decompress the .gz file
- `>`: Redirect output to CSV file
- `outputFiles`: Capture CSV for use in next tasks

### Task 2: Create Staging Table

Creates a temporary staging table with the correct schema.

```yaml
- id: create_staging_table
  type: io.kestra.plugin.jdbc.postgresql.Query
  sql: |
    DROP TABLE IF EXISTS {{ render(vars.staging_table) }};
    
    CREATE TABLE {{ render(vars.staging_table) }} (
      VendorID INT,
      tpep_pickup_datetime TIMESTAMP,
      tpep_dropoff_datetime TIMESTAMP,
      passenger_count DOUBLE PRECISION,
      trip_distance DOUBLE PRECISION,
      RatecodeID DOUBLE PRECISION,
      store_and_fwd_flag TEXT,
      PULocationID INT,
      DOLocationID INT,
      payment_type INT,
      fare_amount DOUBLE PRECISION,
      extra DOUBLE PRECISION,
      mta_tax DOUBLE PRECISION,
      tip_amount DOUBLE PRECISION,
      tolls_amount DOUBLE PRECISION,
      improvement_surcharge DOUBLE PRECISION,
      total_amount DOUBLE PRECISION,
      congestion_surcharge DOUBLE PRECISION,
      airport_fee DOUBLE PRECISION,
      filename TEXT,
      id TEXT
    );
```

**Note:** Schema differs between yellow and green taxis. Adjust columns accordingly.

### Task 3: Load Data to Staging

Loads CSV data into the staging table.

```yaml
- id: load_to_staging
  type: io.kestra.plugin.jdbc.postgresql.CopyIn
  format: CSV
  table: "{{ render(vars.staging_table) }}"
  header: true
  from: "{{ render(vars.data) }}"
  columns:
    - VendorID
    - tpep_pickup_datetime
    - tpep_dropoff_datetime
    - passenger_count
    - trip_distance
    - RatecodeID
    - store_and_fwd_flag
    - PULocationID
    - DOLocationID
    - payment_type
    - fare_amount
    - extra
    - mta_tax
    - tip_amount
    - tolls_amount
    - improvement_surcharge
    - total_amount
    - congestion_surcharge
    - airport_fee
```

### Task 4: Add Unique Identifiers

Adds filename and unique ID to each row to prevent duplicates.

```yaml
- id: add_filename_and_id
  type: io.kestra.plugin.jdbc.postgresql.Query
  sql: |
    UPDATE {{ render(vars.staging_table) }}
    SET 
      filename = '{{ render(vars.file) }}',
      id = md5(
        VendorID::TEXT ||
        tpep_pickup_datetime::TEXT ||
        tpep_dropoff_datetime::TEXT ||
        passenger_count::TEXT ||
        trip_distance::TEXT ||
        PULocationID::TEXT ||
        DOLocationID::TEXT ||
        total_amount::TEXT
      );
```

**Important Discovery:**
Using the `md5()` cryptographic hash function generates a unique identifier for each row based on multiple column values. This prevents duplicate entries when the pipeline is re-executed.

### Task 5: Create Main Table

Creates the main destination table if it doesn't exist.

```yaml
- id: create_main_table
  type: io.kestra.plugin.jdbc.postgresql.Query
  sql: |
    CREATE TABLE IF NOT EXISTS {{ render(vars.table) }} (
      -- Same schema as staging table
      VendorID INT,
      tpep_pickup_datetime TIMESTAMP,
      -- ... (all columns)
      filename TEXT,
      id TEXT PRIMARY KEY
    );
```

### Task 6: Merge to Main Table

Merges staging data into the main table, avoiding duplicates.

```yaml
- id: merge_to_main
  type: io.kestra.plugin.jdbc.postgresql.Query
  sql: |
    MERGE INTO {{ render(vars.table) }} AS main
    USING {{ render(vars.staging_table) }} AS staging
    ON main.id = staging.id
    WHEN NOT MATCHED THEN
      INSERT (VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, ...)
      VALUES (staging.VendorID, staging.tpep_pickup_datetime, ...);
```

**Note:** The `MERGE` statement requires PostgreSQL 15+. Ensure you're using `postgres:latest` or `postgres:15+` in Docker.

### Task 7: Cleanup

Truncates the staging table and purges temporary files.

```yaml
- id: truncate_staging
  type: io.kestra.plugin.jdbc.postgresql.Query
  sql: |
    TRUNCATE TABLE {{ render(vars.staging_table) }};

- id: purge_files
  type: io.kestra.plugin.core.storage.PurgeCurrentExecutionFiles
  disabled: false
```

### Running the Flow

1. Add the flow in Kestra UI
2. Click "Execute"
3. Set inputs (taxi type, year, month)
4. Click "Execute"
5. Monitor execution in Gantt view and logs
6. Verify data in pgAdmin

---

## Part 7: Scheduling and Backfilling

### Adding a Schedule Trigger

Automate the pipeline to run periodically.

```yaml
triggers:
  - id: monthly_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 1 * *"  # First day of each month at 9 AM
    inputs:
      taxi: yellow
      year: "{{ trigger.date | date('yyyy') }}"
      month: "{{ trigger.date | date('MM') }}"
```

**Key Points:**
- `trigger.date`: Automatically provides the schedule execution date
- `| date('yyyy')`: Formats the year
- `| date('MM')`: Formats the month
- Remove year/month from manual inputs since triggers provide them

### Backfilling Historical Data

**Backfill** is the process of running a workflow for historical data that wasn't processed when it originally occurred.

**Steps to Backfill:**
1. Navigate to the flow in Kestra UI
2. Click "Triggers" tab
3. Find your schedule trigger
4. Click "Backfill" button
5. Select date range (e.g., Jan 2019 - Dec 2020)
6. Click "Execute Backfill"

**Important Considerations:**
- Run backfills one at a time if using a single staging table
- Multiple concurrent executions may conflict
- Monitor execution progress in the Executions tab
- Backfills respect the schedule's cron expression

**Example: Backfill 2019 Data**
```
Start Date: 2019-01-01
End Date: 2019-12-31
Schedule: 0 9 1 * * (monthly)
Result: 12 executions (one per month)
```

---

## Part 8: Moving to Google Cloud Platform (GCP)

### Project 3: ETL Pipeline with GCS and BigQuery

This project extends the pipeline to Google Cloud, using:
- **Google Cloud Storage (GCS)**: Data lake for raw files
- **BigQuery**: Data warehouse for analytics

**Benefits of Cloud:**
- Infinitely scalable storage and compute
- No local resource constraints
- Production-ready infrastructure
- Easy to query large datasets

### GCP Prerequisites

**1. Create a GCP Account and Project**
- Sign up at https://cloud.google.com
- Create a new project (e.g., "data-engineering-zoomcamp")

**2. Enable Required APIs**
- Google Cloud Storage API
- BigQuery API

**3. Create a Service Account**
1. Navigate to IAM & Admin → Service Accounts
2. Create a service account (e.g., "kestra-service-account")
3. Grant roles:
   - Storage Admin
   - BigQuery Admin
4. Create and download JSON key file

**4. Set Up KV Store in Kestra**

Store GCP configuration in Kestra's Key-Value Store:

```
Key: GCP_PROJECT_ID
Value: your-project-id

Key: GCP_LOCATION
Value: us-central1

Key: GCP_BUCKET_NAME
Value: your-unique-bucket-name

Key: GCP_DATASET
Value: ny_taxi
```

**5. Store Service Account as Secret**

1. Go to Settings → Secrets in Kestra UI
2. Add new secret:
   - Key: `GCP_SERVICE_ACCOUNT`
   - Value: Paste entire JSON key file content

### Setting Up GCP Resources with Kestra

Create a flow to set up GCS bucket and BigQuery dataset:

```yaml
id: 05_gcp_setup
namespace: zoomcamp

tasks:
  - id: create_gcs_bucket
    type: io.kestra.plugin.gcp.gcs.CreateBucket
    ifExists: SKIP
    storageClass: REGIONAL
    name: "{{ kv('GCP_BUCKET_NAME') }}"
  
  - id: create_bq_dataset
    type: io.kestra.plugin.gcp.bigquery.CreateDataset
    name: "{{ kv('GCP_DATASET') }}"
    ifExists: SKIP

pluginDefaults:
  - type: io.kestra.plugin.gcp
    values:
      serviceAccount: "{{ secret('GCP_SERVICE_ACCOUNT') }}"
      projectId: "{{ kv('GCP_PROJECT_ID') }}"
      location: "{{ kv('GCP_LOCATION') }}"
      bucket: "{{ kv('GCP_BUCKET_NAME') }}"
```

**Run this flow once** to create your GCP resources.

### GCP ETL Flow Structure

**Modified Variables:**
```yaml
variables:
  file: "{{ inputs.taxi }}_tripdata_{{ inputs.year }}-{{ inputs.month }}.csv"
  gcs_path: "raw/{{ inputs.taxi }}/{{ inputs.year }}/{{ render(vars.file) }}"
  staging_table: "{{ kv('GCP_DATASET') }}.{{ inputs.taxi }}_tripdata_staging"
  table: "{{ kv('GCP_DATASET') }}.{{ inputs.taxi }}_tripdata"
```

### Task 1: Extract and Upload to GCS

```yaml
- id: extract
  type: io.kestra.plugin.scripts.shell.Commands
  outputFiles:
    - "*.csv"
  taskRunner:
    type: io.kestra.plugin.core.runner.Process
  commands:
    - wget -qO- https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{{ inputs.taxi }}/{{ render(vars.file) }}.gz | gunzip > {{ render(vars.file) }}

- id: upload_to_gcs
  type: io.kestra.plugin.gcp.gcs.Upload
  from: "{{ render(vars.file) }}"
  to: "{{ render(vars.gcs_path) }}"
```

### Task 2: Create BigQuery Tables

```yaml
- id: create_staging_table
  type: io.kestra.plugin.gcp.bigquery.Query
  sql: |
    CREATE TABLE IF NOT EXISTS {{ render(vars.staging_table) }} (
      VendorID INT64,
      tpep_pickup_datetime TIMESTAMP,
      tpep_dropoff_datetime TIMESTAMP,
      passenger_count FLOAT64,
      trip_distance FLOAT64,
      RatecodeID FLOAT64,
      store_and_fwd_flag STRING,
      PULocationID INT64,
      DOLocationID INT64,
      payment_type INT64,
      fare_amount FLOAT64,
      extra FLOAT64,
      mta_tax FLOAT64,
      tip_amount FLOAT64,
      tolls_amount FLOAT64,
      improvement_surcharge FLOAT64,
      total_amount FLOAT64,
      congestion_surcharge FLOAT64,
      airport_fee FLOAT64,
      filename STRING,
      id STRING
    );
```

**Note:** BigQuery uses `INT64`, `FLOAT64`, `STRING` instead of PostgreSQL types.

### Task 3: Load from GCS to BigQuery

```yaml
- id: load_to_staging
  type: io.kestra.plugin.gcp.bigquery.Load
  destinationTable: "{{ render(vars.staging_table) }}"
  format: CSV
  csvOptions:
    fieldDelimiter: ","
    skipLeadingRows: 1
  from:
    - "{{ render(vars.gcs_path) }}"
  writeDisposition: WRITE_TRUNCATE
```

### Task 4: Add IDs and Merge

```yaml
- id: add_filename_and_id
  type: io.kestra.plugin.gcp.bigquery.Query
  sql: |
    UPDATE {{ render(vars.staging_table) }}
    SET 
      filename = '{{ render(vars.file) }}',
      id = TO_HEX(MD5(
        CAST(VendorID AS STRING) ||
        CAST(tpep_pickup_datetime AS STRING) ||
        CAST(tpep_dropoff_datetime AS STRING) ||
        CAST(passenger_count AS STRING) ||
        CAST(trip_distance AS STRING) ||
        CAST(PULocationID AS STRING) ||
        CAST(DOLocationID AS STRING) ||
        CAST(total_amount AS STRING)
      ))
    WHERE TRUE;

- id: merge_to_main
  type: io.kestra.plugin.gcp.bigquery.Query
  sql: |
    MERGE {{ render(vars.table) }} AS main
    USING {{ render(vars.staging_table) }} AS staging
    ON main.id = staging.id
    WHEN NOT MATCHED THEN
      INSERT (VendorID, tpep_pickup_datetime, ...)
      VALUES (staging.VendorID, staging.tpep_pickup_datetime, ...);
```

### Task 5: Cleanup

```yaml
- id: truncate_staging
  type: io.kestra.plugin.gcp.bigquery.Query
  sql: |
    TRUNCATE TABLE {{ render(vars.staging_table) }};

- id: purge_files
  type: io.kestra.plugin.core.storage.PurgeCurrentExecutionFiles
  disabled: false
```

### Scheduling GCP Pipeline

Create separate schedules for yellow and green taxi data:

```yaml
triggers:
  - id: yellow_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 1 * *"  # 9 AM UTC, 1st of month
    inputs:
      taxi: yellow
      year: "{{ trigger.date | date('yyyy') }}"
      month: "{{ trigger.date | date('MM') }}"
  
  - id: green_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 10 1 * *"  # 10 AM UTC, 1st of month
    inputs:
      taxi: green
      year: "{{ trigger.date | date('yyyy') }}"
      month: "{{ trigger.date | date('MM') }}"
```

### Backfilling in the Cloud

With cloud infrastructure, you can backfill the entire dataset without resource constraints:

1. Navigate to flow triggers
2. Select yellow_schedule
3. Backfill 2019-2020 data (24 months)
4. Repeat for green_schedule
5. Monitor in Executions tab

**Advantage**: Infinitely scalable storage and compute means no local machine limitations.

---

## Part 9: Production Deployment

### Deploying Kestra to GCP

For production use, deploy Kestra to the cloud so it continues orchestrating pipelines without requiring your local machine.

**Deployment Options:**
- Google Cloud Run
- Google Compute Engine
- Google Kubernetes Engine (GKE)
- Docker on VM

### Git Sync for Flows

Automatically sync and deploy workflows from a Git repository:

1. Store flows in Git repository
2. Configure Kestra to sync from Git
3. Flows automatically deploy on push/merge
4. Version control for all workflows

**Benefits:**
- CI/CD integration
- Code review process
- Rollback capability
- Team collaboration

**Important Security Note:**
- Never commit secrets or credentials to Git
- Use KV Store and Secrets for sensitive data
- Keep workflow logic separate from configuration

---

## Part 10: Advanced Kestra Features

### KV Store (Key-Value Store)

A storage system for persisting data as key-value pairs, ideal for configuration that doesn't change often but needs to be accessed across multiple flows.

**Use Cases:**
- Database connection strings
- API endpoints
- Project IDs
- Bucket names
- Dataset names

**Accessing KV Store:**
```yaml
{{ kv('GCP_PROJECT_ID') }}
{{ kv('postgres_host', 'company.infra') }}  # With namespace
```

### Secrets Management

Secure storage for sensitive information like passwords, API keys, and service account credentials.

**Accessing Secrets:**
```yaml
{{ secret('GCP_SERVICE_ACCOUNT') }}
{{ secret('POSTGRES_PASSWORD') }}
{{ secret('API_KEY') }}
```

**Best Practice:** Always use Secrets for sensitive data, never hardcode in flows.

### Concurrency Control

Control how many executions of a flow can run simultaneously.

```yaml
concurrency:
  limit: 1
  behavior: QUEUE
```

**Behaviors:**
- `QUEUE`: Wait for current execution to finish
- `CANCEL`: Cancel new execution
- `FAIL`: Fail new execution

### Error Handling

Define what happens when tasks fail:

```yaml
errors:
  - id: alert_on_failure
    type: io.kestra.plugin.notifications.slack.SlackIncomingWebhook
    url: "{{ secret('SLACK_WEBHOOK') }}"
    payload: |
      {
        "text": "Pipeline failed: {{ flow.id }}"
      }
```

### Retry Logic

Automatically retry failed tasks:

```yaml
- id: flaky_task
  type: io.kestra.plugin.core.http.Download
  uri: "https://api.example.com/data"
  retry:
    maxAttempt: 3
    maxDuration: PT10M
    warningOnRetry: true
```

### Parallel Execution

Run multiple tasks simultaneously:

```yaml
- id: parallel_processing
  type: io.kestra.plugin.core.flow.Parallel
  tasks:
    - id: process_yellow
      type: io.kestra.plugin.core.flow.Subflow
      namespace: zoomcamp
      flowId: taxi_etl
      inputs:
        taxi: yellow
    
    - id: process_green
      type: io.kestra.plugin.core.flow.Subflow
      namespace: zoomcamp
      flowId: taxi_etl
      inputs:
        taxi: green
```

### Subflows

Reuse flows as tasks in other flows:

```yaml
- id: run_subflow
  type: io.kestra.plugin.core.flow.Subflow
  namespace: zoomcamp
  flowId: data_validation
  inputs:
    dataset: "{{ inputs.table }}"
```

---

## Part 11: Working with dbt in Kestra (Optional)

Kestra can orchestrate dbt (data build tool) transformations directly.

### dbt Flow Example

```yaml
id: 03_postgres_dbt
namespace: zoomcamp

inputs:
  - id: dbt_command
    type: SELECT
    values:
      - dbt run
      - dbt test
      - dbt build
    defaults: dbt build

tasks:
  - id: sync_namespace_files
    type: io.kestra.plugin.core.flow.WorkingDirectory
    tasks:
      - id: git_clone
        type: io.kestra.plugin.git.Clone
        url: https://github.com/your-repo/dbt-project
        branch: main
      
      - id: dbt_run
        type: io.kestra.plugin.dbt.cli.DbtCLI
        containerImage: ghcr.io/kestra-io/dbt-duckdb:latest
        commands:
          - "{{ inputs.dbt_command }}"
```

**Benefits:**
- Version-controlled transformations
- Automatic documentation
- Testing and data quality checks
- Integration with orchestration

---

## Part 12: Kestra UI Features

### Topology View

Visual DAG representation of your workflow showing task dependencies and flow.

**Features:**
- Drag-and-drop task editing
- Real-time visualization
- Dependency visualization
- Click to view task details

### Gantt Chart

Timeline view showing when each task runs and how long it takes.

**Use Cases:**
- Identify bottlenecks
- Optimize task order
- Understand execution patterns
- Debug timing issues

### Execution Logs

Detailed logs for every task execution.

**Features:**
- Search and filter logs
- Download logs
- Real-time streaming
- Error highlighting

### Revisions

Every flow change creates a new revision (version).

**Features:**
- View revision history
- Compare revisions
- Rollback to previous version
- Track who made changes

### Namespace Files

Store and manage files used across flows in a namespace.

**Use Cases:**
- SQL query templates
- Python scripts
- Configuration files
- dbt models

---

## Key Takeaways

### Workflow Orchestration
- Orchestration coordinates multiple tasks to work together
- Essential for production data pipelines
- Provides visibility, error handling, and automation

### Kestra Platform
- User-friendly, open-source orchestration tool
- YAML-based workflows (Infrastructure as Code)
- Visual UI with topology and Gantt views
- Extensive plugin ecosystem (1000+ integrations)

### Best Practices
- Use inputs for dynamic, reusable flows
- Store configuration in KV Store
- Secure credentials in Secrets
- Use plugin defaults to avoid repetition
- Implement proper error handling and retries
- Version control flows with Git
- Test locally before deploying to production
- Monitor executions and review logs

### ETL Pipeline Patterns
- **Extract**: Download/fetch data from sources
- **Transform**: Clean, validate, and structure data
- **Load**: Insert into destination (staging → main table pattern)
- **Cleanup**: Remove temporary data and files

### Staging Table Pattern
- Create temporary staging table
- Load data to staging
- Add unique identifiers (MD5 hash)
- Merge to main table (avoiding duplicates)
- Truncate staging for next run

### Scheduling & Backfilling
- Use cron expressions for schedules
- Backfill historical data easily
- Control concurrency to avoid conflicts
- Leverage cloud scalability for large backfills

---

## Additional Resources

### Official Documentation
- [Kestra Documentation](https://kestra.io/docs)
- [Kestra GitHub](https://github.com/kestra-io/kestra)
- [Kestra Blueprints](https://kestra.io/blueprints) - Example workflows
- [Kestra Plugins](https://kestra.io/plugins) - Plugin documentation

### Data Engineering Zoomcamp
- [Course GitHub](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- [YouTube Playlist](https://www.youtube.com/playlist?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)


