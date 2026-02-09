# Data Engineering Zoomcamp - Module 4 Notes

## Part 1: Introduction to Analytics Engineering

### What is Analytics Engineering?

**Analytics Engineering** is a relatively new role in the modern data stack that combines aspects of data engineering and data analysis, focusing on the transformation layer of the data pipeline.

**The Evolution of Data Roles:**

Traditional data teams consist of:
- **Data Engineers**: Build and maintain data infrastructure, pipelines, and systems
- **Data Analysts**: Use existing data to answer business questions and create reports
- **Data Scientists**: Build statistical and machine learning models

**The Gap:**

In traditional setups, there was a disconnect between:
- Data engineers who built pipelines but didn't always understand business context
- Data analysts who understood business needs but lacked engineering skills
- Complex SQL transformations living in BI tools or scattered across different systems

### The Analytics Engineer Role

**Analytics Engineers** bridge this gap by:

1. **Bringing software engineering practices to data transformation**:
   - Version control for data models
   - Code review and collaboration
   - Automated testing
   - CI/CD for analytics code

2. **Owning the transformation layer**:
   - Raw data → Cleaned data → Business logic → Analytics-ready datasets
   - Creating reusable data models
   - Implementing data quality checks

3. **Working at the intersection of engineering and analytics**:
   - Understand business requirements like analysts
   - Apply engineering rigor like data engineers
   - Enable self-service analytics

**Core Responsibilities:**

```
Analytics Engineer Focus Areas:
├── Data Modeling
│   ├── Dimensional modeling (facts & dimensions)
│   ├── Defining grain and relationships
│   └── Creating consistent business logic
├── Data Transformation
│   ├── Staging raw data
│   ├── Applying business rules
│   └── Creating aggregate tables
├── Data Quality
│   ├── Data validation
│   ├── Testing assumptions
│   └── Monitoring data freshness
└── Data Presentation
    ├── Building analytics-ready datasets
    ├── Creating documentation
    └── Enabling BI tools
```

**Skills Required:**
- Strong SQL proficiency
- Understanding of data modeling concepts
- Software engineering fundamentals (Git, testing, documentation)
- Business acumen and stakeholder communication
- Familiarity with data warehousing concepts

---

## Part 2: ETL vs ELT - A Paradigm Shift

### Understanding ETL (Extract, Transform, Load)

**Traditional ETL Workflow:**

```
Source Systems → Extract → Transform (Outside DWH) → Load → Data Warehouse → BI Tools
     ↓              ↓            ↓                      ↓
  Databases    Pull Data    ETL Tool              Insert Data
  APIs         From Source  Transformations        Into DWH
  Files                     (Talend, Informatica)
```

**ETL Characteristics:**

1. **Transform Before Loading**:
   - Data is transformed in a separate processing engine
   - Transformations happen outside the data warehouse
   - Processed data is then loaded into the warehouse

2. **Traditional Tools**:
   - Informatica PowerCenter
   - IBM DataStage
   - Talend
   - SSIS (SQL Server Integration Services)

3. **Historical Context**:
   - Developed when storage was expensive
   - Database compute was limited and costly
   - Warehouse resources needed to be preserved

**ETL Advantages:**
- Data arrives in warehouse already cleaned and formatted
- Reduces warehouse compute load
- Can handle complex transformations before loading

**ETL Disadvantages:**
- Slow development cycle (need to extract data repeatedly for testing)
- Limited flexibility (changing transformations requires re-extracting)
- Black box transformations (hard to debug)
- Vendor lock-in with proprietary tools
- Difficult for analysts to modify logic

### Modern ELT (Extract, Load, Transform)

**ELT Workflow:**

```
Source Systems → Extract → Load → Data Warehouse → Transform (Inside DWH) → BI Tools
     ↓              ↓         ↓           ↓              ↓
  Databases    Pull Data  Insert Raw   BigQuery     dbt Models
  APIs         From Source  Data      Snowflake    SQL Transforms
  Files                                Redshift
```

**ELT Characteristics:**

1. **Load Before Transforming**:
   - Raw data is loaded into the warehouse first
   - Transformations happen using warehouse compute power
   - Leverage SQL for transformations

2. **Modern Stack**:
   - **Extract & Load**: Fivetran, Stitch, Airbyte, Meltano
   - **Transform**: dbt, Dataform
   - **Warehouse**: BigQuery, Snowflake, Redshift, Databricks

3. **Enabled by Modern Cloud Warehouses**:
   - Cheap, scalable storage
   - Powerful compute engines
   - Separation of storage and compute
   - Columnar storage optimizations

**ELT Advantages:**

✅ **Faster Development**:
- No need to repeatedly query source systems
- Iterate on transformations using loaded data
- Quick feedback loops

✅ **Greater Flexibility**:
- Raw data always available
- Can create new transformations without re-extracting
- Easy to modify existing logic

✅ **Transparency**:
- SQL-based transformations are readable
- Clear lineage from source to analytics
- Easy to debug and audit

✅ **Democratized Access**:
- Analysts can write transformations (SQL)
- Version controlled like software
- Self-service analytics

✅ **Cost Effective**:
- Leverage warehouse optimization
- Pay for compute only when transforming
- Storage is cheap

**ELT Disadvantages:**
- Requires robust data warehouse
- Need to manage raw data
- Warehouse costs for compute

### Comparison Table

| Aspect | ETL | ELT |
|--------|-----|-----|
| **Transform Location** | Outside warehouse (ETL tool) | Inside warehouse (SQL) |
| **When Transform Happens** | Before loading | After loading |
| **Primary Tool** | Proprietary ETL platforms | SQL + dbt |
| **Skill Required** | ETL tool expertise | SQL proficiency |
| **Development Speed** | Slower (re-extract for changes) | Faster (iterate on loaded data) |
| **Flexibility** | Limited (fixed transformations) | High (raw data always available) |
| **Transparency** | Low (black box) | High (SQL code) |
| **Version Control** | Difficult | Native (Git integration) |
| **Testing** | Limited | Built-in testing framework |
| **Documentation** | Manual, separate | Auto-generated |
| **Best For** | Legacy systems, compliance | Modern cloud data stacks |
| **Cost Model** | License + infrastructure | Storage + compute on-demand |

**When to Use ETL:**
- Must transform data before loading (e.g., PII masking for compliance)
- Limited warehouse compute capacity
- Legacy systems that require traditional ETL

**When to Use ELT (Modern Recommendation):**
- Cloud-based data warehouse
- Agile analytics requirements
- Teams with SQL skills
- Need for rapid iteration
- Transparency and auditability required

---

## Part 3: Introduction to dbt (data build tool)

### What is dbt?

**dbt** (data build tool) is an open-source command-line tool that enables data analysts and engineers to transform data in their warehouse more effectively.

**Official Definition:**
> "dbt is a transformation workflow that lets teams quickly and collaboratively deploy analytics code following software engineering best practices like modularity, portability, CI/CD, and documentation."

**Core Concept:**

dbt focuses exclusively on the **"T" (Transform)** in ELT:
- **Doesn't extract** data from sources
- **Doesn't load** data into warehouses
- **Only transforms** data that's already in the warehouse

**How dbt Works:**

```
1. You write SQL SELECT statements in .sql files
              ↓
2. dbt compiles them into DDL/DML statements
              ↓
3. dbt executes them against your data warehouse
              ↓
4. Materialized tables/views are created
              ↓
5. Tests run to validate data quality
              ↓
6. Documentation auto-generates
```

### Why dbt?

**Problems dbt Solves:**

1. **Scattered Transformation Logic**:
   - Before: SQL in BI tools, notebooks, cron jobs, random scripts
   - After: Centralized, version-controlled dbt project

2. **No Version Control**:
   - Before: SQL queries lost in BI tools or stored procedures
   - After: Git-based version control for all transformations

3. **No Testing**:
   - Before: Data quality issues discovered by end users
   - After: Automated tests run with every transformation

4. **Poor Documentation**:
   - Before: Tribal knowledge or outdated wikis
   - After: Auto-generated, always up-to-date documentation

5. **Difficult Collaboration**:
   - Before: Copy-paste SQL between analysts
   - After: Modular, reusable models

### dbt Core Features

**1. SQL-Based Transformations**

Write transformations as SELECT statements:

```sql
-- models/staging/stg_orders.sql
SELECT
    order_id,
    customer_id,
    order_date,
    order_total
FROM {{ source('raw', 'orders') }}
WHERE order_date >= '2020-01-01'
```

**2. Jinja Templating**

Add programming logic to SQL:

```sql
-- Use ref() to reference other models
SELECT
    o.order_id,
    c.customer_name,
    o.order_total
FROM {{ ref('stg_orders') }} o
JOIN {{ ref('stg_customers') }} c
    ON o.customer_id = c.customer_id

-- Use macros for reusable logic
WHERE {{ dbt_utils.date_spine(...) }}
```

**3. Materializations**

Control how models are created in the warehouse:

```sql
-- models/core/fact_orders.sql
{{ config(materialized='table') }}

SELECT * FROM {{ ref('stg_orders') }}
```

**Materialization Types:**

| Type | Description | Use Case | Rebuild Strategy |
|------|-------------|----------|------------------|
| **View** | Virtual table (no data stored) | Lightweight transformations | Always rebuild |
| **Table** | Physical table (data stored) | Heavy transformations, frequently queried | Full refresh |
| **Incremental** | Append new records only | Large tables with new data | Append/merge new rows |
| **Ephemeral** | CTE (no database object created) | Intermediate logic | Compiled inline |

**4. Testing**

Built-in data quality tests:

```yaml
# models/schema.yml
models:
  - name: stg_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: customer_id
        tests:
          - relationships:
              to: ref('stg_customers')
              field: customer_id
```

**5. Documentation**

Auto-generated documentation:

```yaml
# models/schema.yml
models:
  - name: stg_orders
    description: Staging table for orders from our ERP system
    columns:
      - name: order_id
        description: Primary key for orders
      - name: order_total
        description: Total order amount in USD
```

**6. DAG (Directed Acyclic Graph)**

dbt automatically builds dependency graph:
- Understands model relationships via `ref()` and `source()`
- Runs models in correct order
- Visualizes lineage

### dbt Versions: Core vs Cloud

**dbt Core (Open Source):**
- Command-line tool
- Free forever
- Runs locally or on servers
- All core functionality included
- Install: `pip install dbt-<adapter>`

**dbt Cloud (Managed Service):**
- Web-based IDE
- Hosted by dbt Labs
- Additional features:
  - Development environment
  - Job scheduler
  - Integrated documentation
  - Metadata API
  - Semantic layer
- Free tier available
- Paid plans for teams

**Comparison:**

| Feature | dbt Core | dbt Cloud |
|---------|----------|-----------|
| **Cost** | Free | Free tier + paid plans |
| **Interface** | Command line | Web IDE + CLI |
| **Deployment** | Self-hosted | Managed |
| **Scheduling** | External (Airflow, cron) | Built-in |
| **IDE** | Your editor (VSCode, etc.) | Web-based IDE |
| **Documentation Hosting** | Self-host | Hosted |
| **Metadata** | Local | Centralized API |
| **Best For** | Engineers, self-hosted setups | Teams, easier setup |

### Supported Data Warehouses

dbt connects to warehouses via **adapters**:

**Official Adapters:**
- ✅ BigQuery (`dbt-bigquery`)
- ✅ Snowflake (`dbt-snowflake`)
- ✅ Redshift (`dbt-redshift`)
- ✅ Databricks (`dbt-databricks`)
- ✅ PostgreSQL (`dbt-postgres`)

**Community Adapters:**
- DuckDB
- MySQL
- SQL Server
- Clickhouse
- Many more...

---

## Part 4: Dimensional Modeling with Kimball Methodology

### Introduction to Dimensional Modeling

**Dimensional Modeling** is a data modeling technique designed specifically for analytics and reporting. It organizes data into **facts** and **dimensions** to make it easy to understand and query.

**Created by Ralph Kimball** in 1996 with "The Data Warehouse Toolkit"

### Why Dimensional Modeling?

**Benefits:**

1. **Query Performance**:
   - Optimized for analytical queries
   - Denormalized structure reduces joins
   - Faster aggregations

2. **Business User Friendly**:
   - Intuitive structure (facts = what happened, dimensions = context)
   - Easy to understand and navigate
   - Aligns with how businesses think

3. **Flexibility**:
   - Easy to add new dimensions
   - Supports changing business questions
   - Extensible design

4. **Consistency**:
   - Single source of truth
   - Conformed dimensions across business processes
   - Standardized metrics

### The Star Schema

**Star Schema** is the fundamental structure in dimensional modeling:

```
                    Dimension Tables (Context)
                           ↓
        ┌─────────────┬──────────┬─────────────┐
        │             │          │             │
   ┌────────┐   ┌─────────┐  ┌────────┐  ┌──────────┐
   │  Date  │   │ Product │  │Customer│  │ Location │
   │  Dim   │   │   Dim   │  │  Dim   │  │   Dim    │
   └────┬───┘   └────┬────┘  └───┬────┘  └────┬─────┘
        │            │           │            │
        └────────────┴───────────┴────────────┘
                     │
              ┌──────┴──────┐
              │  Fact Table │  ← Measures (metrics)
              │ (Sales/Trips│
              │  /Events)   │
              └─────────────┘
```

**Why "Star"?**
- Fact table at the center
- Dimension tables radiate outward
- Looks like a star ⭐

### Fact Tables

**Fact tables** store measurements, metrics, or facts about business events.

**Characteristics:**
- Contains **foreign keys** to dimension tables
- Contains **measures** (numeric facts)
- Large tables (millions to billions of rows)
- Each row represents a **business event** at a specific **grain**

**Example: Taxi Trips Fact Table**

```sql
CREATE TABLE fact_trips (
    -- Foreign Keys (point to dimensions)
    trip_id             STRING PRIMARY KEY,
    pickup_datetime_id  TIMESTAMP,
    pickup_location_id  INT,
    dropoff_location_id INT,
    vendor_id           INT,
    
    -- Measures (numeric facts)
    passenger_count     INT,
    trip_distance       FLOAT,
    fare_amount         FLOAT,
    tip_amount          FLOAT,
    total_amount        FLOAT,
    
    -- Degenerate dimensions (attributes that don't deserve own table)
    payment_type        STRING,
    rate_code           STRING
);
```

**Types of Facts:**

1. **Additive Facts**:
   - Can be summed across all dimensions
   - Examples: revenue, quantity, distance
   - Most common and useful

2. **Semi-Additive Facts**:
   - Can be summed across some dimensions but not all
   - Example: account balance (can't sum across time)
   - Use with caution

3. **Non-Additive Facts**:
   - Cannot be summed at all
   - Examples: ratios, percentages, unit prices
   - Usually derived from other facts

**Factless Fact Tables:**
- Record events without numeric measures
- Track occurrences or relationships
- Example: student attendance (just date + student + class)

### Dimension Tables

**Dimension tables** provide context for facts - the "who, what, where, when, why, how."

**Characteristics:**
- Contain **descriptive attributes**
- Smaller tables (thousands to millions of rows)
- Have a **primary key** referenced by fact tables
- Provide filtering, grouping, and labeling for reports

**Example: Zone Dimension Table**

```sql
CREATE TABLE dim_zones (
    -- Primary Key
    zone_id         INT PRIMARY KEY,
    
    -- Descriptive Attributes
    zone_name       STRING,
    borough         STRING,
    service_zone    STRING,
    
    -- Metadata
    created_at      TIMESTAMP,
    updated_at      TIMESTAMP
);
```

**Example: Date Dimension Table**

```sql
CREATE TABLE dim_date (
    -- Primary Key
    date_id         DATE PRIMARY KEY,
    
    -- Date Attributes
    day_name        STRING,  -- 'Monday'
    day_of_week     INT,     -- 1-7
    day_of_month    INT,     -- 1-31
    day_of_year     INT,     -- 1-365
    
    week_of_year    INT,     -- 1-52
    month_name      STRING,  -- 'January'
    month_number    INT,     -- 1-12
    quarter         INT,     -- 1-4
    year            INT,
    
    -- Business Attributes
    is_weekend      BOOLEAN,
    is_holiday      BOOLEAN,
    fiscal_year     INT,
    fiscal_quarter  INT
);
```

**Common Dimension Types:**

1. **Date/Time Dimensions**:
   - Essential for almost all fact tables
   - Enables time-based analysis
   - Pre-populated with calendar attributes

2. **Location Dimensions**:
   - Geographic hierarchies (Country → State → City)
   - Enables spatial analysis

3. **Product Dimensions**:
   - Product hierarchies (Category → Subcategory → Product)
   - Product attributes

4. **Customer Dimensions**:
   - Customer demographics
   - Customer segments

### The Four-Step Design Process (Kimball)

**Step 1: Select the Business Process**

Identify what business process you're modeling.

**Example Business Processes:**
- Sales transactions
- Taxi trips
- Website visits
- Order fulfillment
- Customer support tickets

**Questions to ask:**
- What business process are stakeholders most interested in?
- What events do we need to analyze?
- What decisions will this data support?

**Step 2: Declare the Grain**

Define what each row in the fact table represents - the **level of detail**.

**Grain Examples:**
- "One row per taxi trip" ✅ (atomic grain)
- "One row per customer order line item" ✅ (atomic grain)
- "One row per product per day" ⚠️ (aggregated grain)

**Best Practice: Choose the Most Atomic Grain**
- Store data at the lowest level of detail
- Provides maximum flexibility
- Can always aggregate up, can't disaggregate down

**Common Grain Mistakes:**
```
❌ "One row per order" when you need line items
✅ "One row per order line item"

❌ "Daily sales totals" when you need hourly breakdowns
✅ "One row per transaction"
```

**Step 3: Identify the Dimensions**

Based on the grain, determine what dimensions provide context.

**For "One row per taxi trip" grain:**
- 📅 Pickup Date/Time
- 📍 Pickup Location (Zone)
- 📍 Dropoff Location (Zone)
- 🚕 Vendor
- 👤 Rate Code
- 💳 Payment Type

**Questions to ask:**
- How will business users want to filter the data?
- How will they want to group the data?
- What context is needed to understand the facts?

**Step 4: Identify the Facts**

Determine the numeric measurements for the grain.

**For "One row per taxi trip" grain:**
- 🔢 Passenger Count
- 📏 Trip Distance
- 💰 Fare Amount
- 💵 Tip Amount
- 💳 Total Amount
- ⏱️ Trip Duration

**Questions to ask:**
- What numeric values are being measured?
- What calculations do business users need?
- Are these facts additive, semi-additive, or non-additive?

### Kimball vs Inmon Methodologies

| Aspect | Kimball (Dimensional) | Inmon (Corporate Information Factory) |
|--------|----------------------|---------------------------------------|
| **Approach** | Bottom-up (business process first) | Top-down (enterprise model first) |
| **Data Model** | Denormalized (star schema) | Normalized (3NF) |
| **Build Strategy** | Incremental, one process at a time | Complete enterprise model upfront |
| **Time to Value** | Fast (weeks to months) | Slow (months to years) |
| **User Focus** | Business users and analysts | Enterprise data architecture |
| **Complexity** | Simpler, easier to understand | Complex, harder to query |
| **Flexibility** | High (easy to add dimensions) | Lower (schema changes are hard) |
| **Adoption** | Widely used in analytics | Used in large enterprises |

**Modern Consensus:**
- Kimball methodology dominates analytics
- Star schema is standard for BI tools
- Inmon useful for enterprise data governance

---

## Part 5: dbt Project Structure and Setup

### Anatomy of a dbt Project

**Standard dbt Project Directory Structure:**

```
my_dbt_project/
├── dbt_project.yml          # Project configuration
├── profiles.yml             # Database connection settings
│
├── models/                  # SQL transformation files
│   ├── staging/            # Staging layer (raw → clean)
│   │   ├── schema.yml
│   │   ├── stg_green_tripdata.sql
│   │   └── stg_yellow_tripdata.sql
│   │
│   ├── core/               # Core layer (business logic)
│   │   ├── schema.yml
│   │   ├── dim_zones.sql
│   │   └── fact_trips.sql
│   │
│   └── marts/              # Data marts (final analytics)
│       ├── schema.yml
│       └── monthly_revenue.sql
│
├── macros/                  # Reusable SQL functions
│   └── custom_functions.sql
│
├── seeds/                   # CSV files to load
│   └── taxi_zone_lookup.csv
│
├── tests/                   # Custom tests
│   └── assert_positive_fare.sql
│
├── snapshots/              # Slowly Changing Dimensions
│   └── zones_snapshot.sql
│
├── analyses/               # Ad-hoc queries (not built)
│   └── exploration.sql
│
└── target/                 # Compiled SQL (git-ignored)
    └── compiled/
```

### Key Configuration Files

**1. dbt_project.yml**

Main project configuration:

```yaml
# Project metadata
name: 'taxi_rides_ny'
version: '1.0.0'
config-version: 2

# Profile to use (connects to database)
profile: 'taxi_rides_ny'

# Directories
model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

# Output directory
target-path: "target"
clean-targets: ["target", "dbt_packages"]

# Model configurations
models:
  taxi_rides_ny:
    # Staging models as views
    staging:
      +materialized: view
      +schema: staging
    
    # Core models as tables
    core:
      +materialized: table
      +schema: core
```

**2. profiles.yml**

Database connection configuration (usually in `~/.dbt/`):

```yaml
taxi_rides_ny:  # Profile name (matches dbt_project.yml)
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: my-gcp-project
      dataset: dbt_dev
      location: US
      keyfile: /path/to/service-account-key.json
      threads: 4
      timeout_seconds: 300
    
    prod:
      type: bigquery
      method: service-account
      project: my-gcp-project
      dataset: dbt_prod
      location: US
      keyfile: /path/to/prod-service-account-key.json
      threads: 8
      timeout_seconds: 300
```

**Connection for PostgreSQL:**

```yaml
taxi_rides_ny:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: postgres
      password: postgres
      port: 5432
      dbname: ny_taxi
      schema: dbt_dev
      threads: 4
```

### Setting Up dbt Locally

**Prerequisites:**
- Python 3.7+
- Database (BigQuery, PostgreSQL, etc.)
- Service account credentials (for BigQuery)

**Step 1: Install dbt**

```bash
# Install dbt for BigQuery
pip install dbt-bigquery

# Or for PostgreSQL
pip install dbt-postgres

# Verify installation
dbt --version
```

**Step 2: Initialize Project**

```bash
# Create new dbt project
dbt init taxi_rides_ny

# Navigate to project
cd taxi_rides_ny
```

**Step 3: Configure Connection**

Edit `~/.dbt/profiles.yml` with your database credentials.

**Step 4: Test Connection**

```bash
# Test database connection
dbt debug

# Expected output:
# Connection test: OK connection ok
```

**Step 5: Run Example Models**

```bash
# Run the example models
dbt run

# Run tests
dbt test

# Generate documentation
dbt docs generate
dbt docs serve  # Opens documentation in browser
```

---

## Part 6: dbt Models - Staging Layer

### The Staging Layer Concept

The **staging layer** is the first transformation layer in dbt, where you:
1. Select from raw source tables
2. Apply light transformations (renaming, casting, filtering)
3. Create a clean foundation for downstream models

**Purpose of Staging Models:**

```
Raw Data (Source)  →  Staging Models  →  Core Models  →  Marts
      ↓                     ↓                  ↓              ↓
Messy column      Clean, renamed     Business      Analytics-ready
names, mixed      columns, typed     logic,        aggregations
data types        correctly          joins
```

**Staging Layer Principles:**

1. **One staging model per source table**
2. **Light transformations only**: rename, cast, simple filters
3. **No joins** between tables
4. **No aggregations**
5. **Materialized as views** (ephemeral or view)
6. **1:1 relationship** with source tables

### Sources in dbt

**Sources** define your raw data tables in dbt:

```yaml
# models/staging/schema.yml
version: 2

sources:
  - name: raw_data
    database: my_project
    schema: raw
    tables:
      - name: green_tripdata
        description: Raw green taxi trip data from TLC
        
      - name: yellow_tripdata
        description: Raw yellow taxi trip data from TLC
      
      - name: zones
        description: Taxi zone lookup table
```

**Reference sources in models:**

```sql
-- Instead of hardcoding table names:
SELECT * FROM my_project.raw.green_tripdata  ❌

-- Use source() function:
SELECT * FROM {{ source('raw_data', 'green_tripdata') }}  ✅
```

**Benefits of sources:**
- ✅ Centralized documentation
- ✅ Easy to change schemas/databases
- ✅ Enables source freshness checks
- ✅ Better lineage in documentation

### Creating Staging Models

**Example: Staging Green Taxi Data**

```sql
-- models/staging/stg_green_tripdata.sql

{{ config(materialized='view') }}

SELECT
    -- Identifiers
    {{ dbt_utils.generate_surrogate_key(['vendorid', 'lpep_pickup_datetime']) }} AS trip_id,
    CAST(vendorid AS INTEGER) AS vendor_id,
    CAST(ratecodeid AS INTEGER) AS rate_code_id,
    CAST(pulocationid AS INTEGER) AS pickup_location_id,
    CAST(dolocationid AS INTEGER) AS dropoff_location_id,
    
    -- Timestamps
    CAST(lpep_pickup_datetime AS TIMESTAMP) AS pickup_datetime,
    CAST(lpep_dropoff_datetime AS TIMESTAMP) AS dropoff_datetime,
    
    -- Trip info
    CAST(passenger_count AS INTEGER) AS passenger_count,
    CAST(trip_distance AS NUMERIC) AS trip_distance,
    
    -- Payment info
    CAST(fare_amount AS NUMERIC) AS fare_amount,
    CAST(extra AS NUMERIC) AS extra,
    CAST(mta_tax AS NUMERIC) AS mta_tax,
    CAST(tip_amount AS NUMERIC) AS tip_amount,
    CAST(tolls_amount AS NUMERIC) AS tolls_amount,
    CAST(improvement_surcharge AS NUMERIC) AS improvement_surcharge,
    CAST(total_amount AS NUMERIC) AS total_amount,
    CAST(payment_type AS INTEGER) AS payment_type,
    
    -- Additional fields
    CAST(trip_type AS INTEGER) AS trip_type,
    CAST(congestion_surcharge AS NUMERIC) AS congestion_surcharge,
    
    -- Metadata
    'green' AS service_type

FROM {{ source('raw_data', 'green_tripdata') }}

-- Data quality filters
WHERE vendorid IS NOT NULL
```

**Key Patterns in Staging Models:**

1. **Generate Surrogate Keys**:
```sql
-- Using dbt_utils package
{{ dbt_utils.generate_surrogate_key(['col1', 'col2']) }} AS id
```

2. **Explicit Type Casting**:
```sql
CAST(passenger_count AS INTEGER) AS passenger_count
CAST(fare_amount AS NUMERIC) AS fare_amount
```

3. **Column Renaming**:
```sql
-- Raw: DOLocationID (inconsistent naming)
-- Staged: dropoff_location_id (snake_case, descriptive)
CAST(dolocationid AS INTEGER) AS dropoff_location_id
```

4. **Add Metadata Columns**:
```sql
'green' AS service_type  -- Identify data source
CURRENT_TIMESTAMP() AS loaded_at  -- When processed
```

5. **Basic Data Quality Filters**:
```sql
WHERE vendor_id IS NOT NULL
  AND pickup_datetime >= '2019-01-01'
```

### Staging Model Best Practices

**DO:**
✅ Keep staging models simple
✅ Use one staging model per source
✅ Rename columns to consistent naming convention
✅ Cast data types explicitly
✅ Add basic NULL filters
✅ Document column meanings
✅ Materialize as views (lightweight)

**DON'T:**
❌ Join tables in staging
❌ Aggregate data
❌ Apply complex business logic
❌ Create derived metrics
❌ Materialize as tables (unless necessary)

### Schema Documentation

Document your staging models:

```yaml
# models/staging/schema.yml
version: 2

models:
  - name: stg_green_tripdata
    description: Staging model for green taxi trip data
    columns:
      - name: trip_id
        description: Unique identifier for each trip (surrogate key)
        tests:
          - unique
          - not_null
      
      - name: vendor_id
        description: Provider code (1=Creative Mobile, 2=VeriFone)
        tests:
          - accepted_values:
              values: [1, 2]
      
      - name: pickup_datetime
        description: Start time of the trip
        tests:
          - not_null
      
      - name: total_amount
        description: Total amount charged to passenger (USD)
        tests:
          - not_null
          - dbt_utils.expression_is_true:
              expression: ">= 0"
```

---

## Part 7: dbt Models - Core Layer

### The Core Layer Concept

The **core layer** contains your dimensional models - facts and dimensions - where business logic is applied.

**Purpose of Core Models:**

```
Staging Models  →  Core Models (Facts & Dims)  →  Marts
      ↓                    ↓                          ↓
Clean data      Apply business logic          Final analytics
               Join tables                    datasets
               Create dimensions
               Build facts
```

**Core Layer Characteristics:**

1. **Contains dimensional models** (facts and dimensions)
2. **Applies business logic** and transformations
3. **Joins staging models** together
4. **Materialized as tables** (for performance)
5. **Tested rigorously**
6. **Production-ready datasets**

### Creating Dimension Models

**Example: Zone Dimension**

```sql
-- models/core/dim_zones.sql

{{ config(materialized='table') }}

SELECT
    location_id AS zone_id,
    borough,
    zone AS zone_name,
    service_zone
FROM {{ ref('taxi_zone_lookup') }}  -- Seed file
```

**Note:** This dimension comes from a seed file (static reference data).

**Example: Date Dimension (Generated)**

```sql
-- models/core/dim_date.sql

{{ config(materialized='table') }}

WITH date_spine AS (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2019-01-01' as date)",
        end_date="cast('2025-12-31' as date)"
    )}}
)

SELECT
    date_day,
    EXTRACT(YEAR FROM date_day) AS year,
    EXTRACT(MONTH FROM date_day) AS month,
    EXTRACT(DAY FROM date_day) AS day,
    EXTRACT(DAYOFWEEK FROM date_day) AS day_of_week,
    FORMAT_DATE('%A', date_day) AS day_name,
    FORMAT_DATE('%B', date_day) AS month_name,
    EXTRACT(QUARTER FROM date_day) AS quarter,
    
    -- Calculated fields
    CASE 
        WHEN EXTRACT(DAYOFWEEK FROM date_day) IN (1, 7) 
        THEN TRUE 
        ELSE FALSE 
    END AS is_weekend

FROM date_spine
```

### Creating Fact Models

Fact models join staging models and apply business logic.

**Example: Trips Fact Table**

```sql
-- models/core/fact_trips.sql

{{ config(materialized='table') }}

WITH green_tripdata AS (
    SELECT *,
        'Green' AS service_type
    FROM {{ ref('stg_green_tripdata') }}
),

yellow_tripdata AS (
    SELECT *,
        'Yellow' AS service_type  
    FROM {{ ref('stg_yellow_tripdata') }}
),

trips_unioned AS (
    SELECT * FROM green_tripdata
    UNION ALL
    SELECT * FROM yellow_tripdata
),

dim_zones AS (
    SELECT * FROM {{ ref('dim_zones') }}
)

SELECT 
    trips_unioned.trip_id,
    trips_unioned.vendor_id,
    trips_unioned.service_type,
    trips_unioned.rate_code_id,
    trips_unioned.pickup_location_id,
    trips_unioned.pickup_zone.zone_name AS pickup_zone,
    trips_unioned.pickup_zone.borough AS pickup_borough,
    trips_unioned.dropoff_location_id,
    trips_unioned.dropoff_zone.zone_name AS dropoff_zone,
    trips_unioned.dropoff_zone.borough AS dropoff_borough,
    trips_unioned.pickup_datetime,
    trips_unioned.dropoff_datetime,
    trips_unioned.passenger_count,
    trips_unioned.trip_distance,
    trips_unioned.trip_type,
    trips_unioned.fare_amount,
    trips_unioned.extra,
    trips_unioned.mta_tax,
    trips_unioned.tip_amount,
    trips_unioned.tolls_amount,
    trips_unioned.improvement_surcharge,
    trips_unioned.total_amount,
    trips_unioned.payment_type,
    trips_unioned.congestion_surcharge

FROM trips_unioned
INNER JOIN dim_zones AS pickup_zone
    ON trips_unioned.pickup_location_id = pickup_zone.zone_id
INNER JOIN dim_zones AS dropoff_zone
    ON trips_unioned.dropoff_location_id = dropoff_zone.zone_id
```

**Key Patterns in Fact Models:**

1. **Union Multiple Sources**:
```sql
WITH green AS (SELECT *, 'Green' AS type FROM {{ ref('stg_green') }}),
     yellow AS (SELECT *, 'Yellow' AS type FROM {{ ref('stg_yellow') }})

SELECT * FROM green
UNION ALL
SELECT * FROM yellow
```

2. **Join with Dimensions**:
```sql
FROM facts
JOIN {{ ref('dim_zones') }} AS pickup_zone
    ON facts.pickup_location_id = pickup_zone.zone_id
```

3. **Calculate Derived Metrics**:
```sql
TIMESTAMP_DIFF(dropoff_datetime, pickup_datetime, MINUTE) AS trip_duration_minutes
```

4. **Apply Business Rules**:
```sql
CASE 
    WHEN fare_amount < 0 THEN 0  -- Fix data quality issues
    ELSE fare_amount
END AS fare_amount
```

### Using ref() for Dependencies

The `ref()` function is central to dbt:

```sql
-- Reference a staging model
FROM {{ ref('stg_orders') }}

-- Reference a dimension
JOIN {{ ref('dim_customers') }}
    ON orders.customer_id = customers.customer_id
```

**How ref() works:**

1. **Builds DAG**: dbt tracks dependencies automatically
2. **Runs in order**: Upstream models built before downstream
3. **Environment-aware**: Points to correct schema (dev/prod)
4. **Enables testing**: Can test model dependencies

**Example DAG:**

```
seeds/taxi_zone_lookup.csv
         ↓
    dim_zones  ←──────────────┐
         ↓                     │
stg_green_tripdata → fact_trips
         ↓                     │
stg_yellow_tripdata ──────────┘
```

---

## Part 8: dbt Macros and Packages

### Macros in dbt

**Macros** are reusable SQL functions written in Jinja.

**Creating a Macro:**

```sql
-- macros/get_payment_type_description.sql

{% macro get_payment_type_description(payment_type) %}

    CASE {{ payment_type }}
        WHEN 1 THEN 'Credit card'
        WHEN 2 THEN 'Cash'
        WHEN 3 THEN 'No charge'
        WHEN 4 THEN 'Dispute'
        WHEN 5 THEN 'Unknown'
        WHEN 6 THEN 'Voided trip'
        ELSE 'EMPTY'
    END

{% endmacro %}
```

**Using a Macro:**

```sql
-- In a model
SELECT
    payment_type,
    {{ get_payment_type_description('payment_type') }} AS payment_type_description,
    SUM(total_amount) AS total_revenue
FROM {{ ref('fact_trips') }}
GROUP BY payment_type
```

**Built-in Macros:**

dbt provides many built-in macros:

```sql
-- ref() - reference models
{{ ref('model_name') }}

-- source() - reference sources
{{ source('source_name', 'table_name') }}

-- config() - configure models
{{ config(materialized='table') }}

-- var() - use variables
{{ var('start_date') }}
```

### dbt Packages

**Packages** are collections of macros and models you can import.

**Installing Packages:**

Create `packages.yml` in project root:

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  
  - package: calogica/dbt_expectations
    version: 0.9.0
  
  - package: dbt-labs/codegen
    version: 0.11.0
```

Install packages:

```bash
dbt deps
```

**Popular Packages:**

1. **dbt_utils** - Utility macros:
```sql
-- Generate surrogate key
{{ dbt_utils.generate_surrogate_key(['col1', 'col2']) }}

-- Date spine
{{ dbt_utils.date_spine(...) }}

-- Union tables
{{ dbt_utils.union_relations(relations=[ref('table1'), ref('table2')]) }}

-- Pivot
{{ dbt_utils.pivot(...) }}
```

2. **dbt_expectations** - Data quality tests:
```yaml
tests:
  - dbt_expectations.expect_column_values_to_be_between:
      min_value: 0
      max_value: 100
```

3. **codegen** - Generate dbt code:
```sql
-- Generate source YAML
{{ codegen.generate_source('schema_name') }}

-- Generate base model
{{ codegen.generate_base_model('source_name', 'table_name') }}
```

### Variables in dbt

**Variables** allow you to parameterize your models.

**Defining Variables:**

In `dbt_project.yml`:

```yaml
vars:
  start_date: '2019-01-01'
  is_test_run: false
  payment_type_values: [1, 2, 3, 4, 5, 6]
```

**Using Variables:**

```sql
-- In models
WHERE pickup_datetime >= '{{ var("start_date") }}'

{% if var("is_test_run", default=false) %}
  LIMIT 100
{% endif %}
```

**Override Variables at Runtime:**

```bash
dbt run --vars '{"is_test_run": true}'
```

**Practical Example:**

```sql
-- models/core/fact_trips.sql

{{ config(
    materialized='incremental',
    unique_key='trip_id'
) }}

SELECT *
FROM {{ ref('stg_trips') }}

{% if is_incremental() %}
    WHERE pickup_datetime > (SELECT MAX(pickup_datetime) FROM {{ this }})
{% endif %}

-- For testing, limit results
{% if var("is_test_run", default=false) %}
    LIMIT 100
{% endif %}
```

---

## Part 9: Testing in dbt

### Why Test Data?

**Data quality issues are expensive:**
- ❌ Incorrect business decisions
- ❌ Loss of trust in data
- ❌ Wasted analyst time debugging
- ❌ Incorrect reports to stakeholders

**dbt tests ensure:**
- ✅ Data integrity
- ✅ Business rule compliance
- ✅ Consistency across models
- ✅ Early detection of issues

### Types of Tests in dbt

**1. Schema Tests (Generic Tests)**

Defined in YAML, run against columns.

```yaml
# models/schema.yml
models:
  - name: stg_trips
    columns:
      - name: trip_id
        tests:
          - unique
          - not_null
      
      - name: vendor_id
        tests:
          - accepted_values:
              values: [1, 2]
      
      - name: pickup_location_id
        tests:
          - relationships:
              to: ref('dim_zones')
              field: zone_id
```

**Built-in Schema Tests:**

| Test | Description | Example |
|------|-------------|---------|
| `unique` | Column values are unique | `trip_id` |
| `not_null` | Column has no NULL values | `pickup_datetime` |
| `accepted_values` | Column values in allowed list | `vendor_id IN (1, 2)` |
| `relationships` | Foreign key constraint | References `dim_zones` |

**2. Data Tests (Singular Tests)**

Custom SQL tests in `tests/` directory.

```sql
-- tests/assert_positive_fare_amounts.sql

-- This test will fail if any records are returned
SELECT
    trip_id,
    fare_amount
FROM {{ ref('fact_trips') }}
WHERE fare_amount < 0
```

```sql
-- tests/assert_valid_trip_distance.sql

SELECT
    trip_id,
    trip_distance
FROM {{ ref('fact_trips') }}
WHERE trip_distance < 0
   OR trip_distance > 500  -- Unreasonably long
```

**How Tests Work:**

1. dbt runs the test query
2. If query returns **zero rows** → Test passes ✅
3. If query returns **any rows** → Test fails ❌
4. Failed rows are logged

### Running Tests

```bash
# Run all tests
dbt test

# Run tests for specific model
dbt test --select stg_trips

# Run tests for model and its dependencies
dbt test --select +stg_trips

# Run tests for model and downstream models
dbt test --select stg_trips+

# Run specific test
dbt test --select unique_stg_trips_trip_id
```

**Test Output:**

```
Running with dbt=1.5.0
Found 5 models, 12 tests, 0 snapshots

Completed successfully
Done. PASS=12 WARN=0 ERROR=0 SKIP=0 TOTAL=12
```

### Advanced Testing with dbt_expectations

Install `dbt_expectations` package for more tests:

```yaml
# models/schema.yml
models:
  - name: fact_trips
    tests:
      # Row count tests
      - dbt_expectations.expect_table_row_count_to_be_between:
          min_value: 100000
          max_value: 10000000
      
    columns:
      - name: fare_amount
        tests:
          # Value range test
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              max_value: 1000
          
          # Quantile test
          - dbt_expectations.expect_column_quantile_values_to_be_between:
              quantile: 0.95
              min_value: 0
              max_value: 100
      
      - name: pickup_datetime
        tests:
          # Recency test
          - dbt_expectations.expect_column_max_to_be_between:
              max_value: "current_date()"
              interval: 7
              date_part: day
```

### Testing Best Practices

**DO:**
✅ Test primary keys (unique + not_null)
✅ Test foreign key relationships
✅ Test accepted values for categorical columns
✅ Test numeric ranges for amounts/quantities
✅ Test date ranges
✅ Test business logic assumptions
✅ Run tests in CI/CD pipeline

**DON'T:**
❌ Over-test (every column doesn't need every test)
❌ Write tests that duplicate each other
❌ Forget to test custom logic
❌ Skip testing staging models

**Recommended Testing Strategy:**

```
Staging Models:
  - unique + not_null on primary keys
  - accepted_values for known categories
  - Basic range checks

Core Models:
  - All staging tests
  - relationships (foreign keys)
  - Custom business logic tests
  - Row count checks

Marts:
  - Validate final metrics
  - Ensure no negative values
  - Check date ranges
```

---

## Part 10: Documentation in dbt

### Why Document?

**Problems without documentation:**
- ❌ Tribal knowledge lost when people leave
- ❌ Analysts don't know what data means
- ❌ Duplicate effort (people rebuild existing models)
- ❌ Errors from misunderstanding data

**Benefits of dbt documentation:**
- ✅ Self-service analytics
- ✅ Onboarding new team members
- ✅ Lineage and impact analysis
- ✅ Always up-to-date (code-adjacent docs)

### Adding Descriptions

**In schema.yml:**

```yaml
# models/schema.yml
models:
  - name: fact_trips
    description: >
      Core fact table containing taxi trip records from both
      yellow and green taxi services. Each row represents one
      completed trip with associated metrics and foreign keys
      to dimension tables.
    
    columns:
      - name: trip_id
        description: >
          Surrogate key generated from vendor_id and pickup_datetime.
          Ensures uniqueness across both taxi services.
        tests:
          - unique
          - not_null
      
      - name: service_type
        description: Type of taxi service (Yellow or Green)
        tests:
          - accepted_values:
              values: ['Yellow', 'Green']
      
      - name: total_amount
        description: >
          Total amount charged to passenger including fare, taxes,
          tolls, and surcharges. Expressed in USD.
      
      - name: pickup_zone
        description: Name of the pickup zone (from dim_zones)
```

**For Sources:**

```yaml
# models/staging/schema.yml
sources:
  - name: raw_data
    description: Raw data loaded from NYC TLC website
    schema: raw
    
    tables:
      - name: green_tripdata
        description: >
          Green taxi trip records. Green taxis are permitted to
          pick up passengers in outer boroughs and northern Manhattan.
        
        columns:
          - name: vendorid
            description: Provider code (1=Creative Mobile, 2=VeriFone)
          
          - name: lpep_pickup_datetime
            description: Date and time when meter was engaged
          
          - name: lpep_dropoff_datetime
            description: Date and time when meter was disengaged
```

### Generating Documentation

**Step 1: Generate Docs**

```bash
dbt docs generate
```

This creates:
- `target/catalog.json` - Data profile (row counts, column types)
- `target/manifest.json` - Project structure and lineage
- `target/run_results.json` - Test results

**Step 2: Serve Docs**

```bash
dbt docs serve
```

Opens documentation website in browser at `http://localhost:8080`

### Documentation Website Features

**1. Project Overview**
- All models, sources, tests
- Searchable
- Filterable by schema/package

**2. Model Details**
- Description
- Columns with types and descriptions
- Tests configured
- SQL code (compiled and raw)
- Statistics (row count, etc.)

**3. Lineage Graph (DAG)**
- Visual representation of dependencies
- Click to navigate between models
- See upstream and downstream impacts

**Example Lineage:**

```
taxi_zone_lookup (seed)
        ↓
    dim_zones
        ↓
   ┌────┴────┐
   ↓         ↓
stg_green  stg_yellow
   ↓         ↓
   └────┬────┘
        ↓
   fact_trips
        ↓
  monthly_revenue
```

**4. Column Lineage**
- Trace column from source through transformations
- See where column is used downstream
- Understand impact of changes

### Doc Blocks

For longer documentation, use doc blocks:

```sql
-- models/docs.md

{% docs fact_trips_description %}

# Trips Fact Table

This is the core fact table for taxi trip analysis.

## Grain
One row per completed trip (atomic grain)

## Data Sources
- Green taxi trips from TLC
- Yellow taxi trips from TLC

## Update Frequency
Daily incremental load at 2 AM EST

## Known Issues
- Pre-2019 data may have inconsistent vendor codes
- Some trips have negative fares (data quality issue in source)

## Example Queries

Find average tip by borough:
```sql
SELECT
    pickup_borough,
    AVG(tip_amount) AS avg_tip
FROM {{ ref('fact_trips') }}
GROUP BY pickup_borough
ORDER BY avg_tip DESC
```

{% enddocs %}
```

**Reference in schema.yml:**

```yaml
models:
  - name: fact_trips
    description: '{{ doc("fact_trips_description") }}'
```

### Documentation Best Practices

**DO:**
✅ Document all models and columns
✅ Explain business logic
✅ Note known data quality issues
✅ Provide example queries
✅ Keep docs close to code (schema.yml)
✅ Update docs when changing models
✅ Include metrics definitions

**DON'T:**
❌ Document only complex models
❌ Write documentation separately (it gets outdated)
❌ Use jargon without explanation
❌ Forget to regenerate after changes

---

## Part 11: Deployment and Production

### Development vs Production

**Development Environment:**
- Personal schema (e.g., `dbt_alice_dev`)
- Iterate quickly
- Test changes
- Safe to break things

**Production Environment:**
- Shared schema (e.g., `dbt_prod`)
- Scheduled runs
- Stakeholders depend on it
- Must be reliable

### CI/CD for dbt

**Continuous Integration (CI):**

Test pull requests before merging:

```yaml
# .github/workflows/ci.yml
name: dbt CI

on: pull_request

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      
      - name: Install dbt
        run: pip install dbt-bigquery
      
      - name: Run dbt
        run: |
          dbt deps
          dbt run --target ci
          dbt test --target ci
        env:
          DBT_PROFILES_DIR: .
```

**Benefits:**
- ✅ Catch errors before production
- ✅ Ensure tests pass
- ✅ Validate SQL compiles
- ✅ Prevent broken merges

**Continuous Deployment (CD):**

Deploy to production on merge:

```yaml
# .github/workflows/cd.yml
name: dbt Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
      
      - name: Install dbt
        run: pip install dbt-bigquery
      
      - name: Deploy
        run: |
          dbt deps
          dbt run --target prod
          dbt test --target prod
          dbt docs generate --target prod
```

### Scheduling dbt Jobs

**Option 1: dbt Cloud**

Built-in scheduler:
1. Create job in dbt Cloud
2. Set schedule (cron or interval)
3. Define commands to run
4. Configure alerts

**Option 2: Airflow**

```python
# dags/dbt_dag.py
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'analytics',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'dbt_production',
    default_args=default_args,
    schedule_interval='0 2 * * *',  # 2 AM daily
    catchup=False
) as dag:

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /path/to/dbt && dbt run --target prod'
    )
    
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /path/to/dbt && dbt test --target prod'
    )
    
    dbt_docs = BashOperator(
        task_id='dbt_docs',
        bash_command='cd /path/to/dbt && dbt docs generate --target prod'
    )
    
    dbt_run >> dbt_test >> dbt_docs
```

**Option 3: Prefect**

```python
from prefect import flow, task
import subprocess

@task
def run_dbt_command(command: str):
    result = subprocess.run(
        f"dbt {command}",
        shell=True,
        capture_output=True
    )
    return result.returncode == 0

@flow
def dbt_production_flow():
    run_dbt_command("deps")
    run_dbt_command("run --target prod")
    run_dbt_command("test --target prod")
    run_dbt_command("docs generate --target prod")

if __name__ == "__main__":
    dbt_production_flow()
```

### Incremental Models

For large tables, use incremental materialization:

```sql
-- models/core/fact_trips_incremental.sql

{{
  config(
    materialized='incremental',
    unique_key='trip_id',
    on_schema_change='fail'
  )
}}

SELECT
    trip_id,
    pickup_datetime,
    dropoff_datetime,
    total_amount,
    -- ... other columns
FROM {{ ref('stg_trips') }}

{% if is_incremental() %}
    -- Only process new records
    WHERE pickup_datetime > (
        SELECT MAX(pickup_datetime)
        FROM {{ this }}
    )
{% endif %}
```

**How Incremental Works:**

First run:
```sql
CREATE TABLE fact_trips AS
SELECT * FROM staging_trips
```

Subsequent runs:
```sql
INSERT INTO fact_trips
SELECT * FROM staging_trips
WHERE pickup_datetime > (SELECT MAX(pickup_datetime) FROM fact_trips)
```

**Incremental Strategies:**

1. **Append** (default):
```sql
config(
    materialized='incremental',
    unique_key='id'
)
```

2. **Merge** (upsert):
```sql
config(
    materialized='incremental',
    unique_key='id',
    merge_update_columns=['status', 'updated_at']
)
```

3. **Delete+Insert**:
```sql
config(
    materialized='incremental',
    unique_key='id',
    incremental_strategy='delete+insert'
)
```

## Part 12: Integration with BI Tools

### Connecting dbt to Looker/Data Studio

After building dbt models, you visualize them in BI tools.

**Google Looker Studio (formerly Data Studio):**

1. **Connect to BigQuery**:
   - Create new report
   - Select BigQuery connector
   - Choose your dbt project dataset
   - Select fact tables (e.g., `fact_trips`)

2. **Create Visualizations**:
   - Time series: trips by date
   - Bar charts: trips by borough
   - Scorecards: total revenue
   - Maps: trips by zone

3. **Best Practices**:
   - Use aggregate models from dbt (not raw facts)
   - Create dbt marts specifically for dashboards
   - Pre-calculate metrics in dbt (faster BI)

**Example: Mart for Dashboard**

```sql
-- models/marts/dashboard_monthly_metrics.sql

{{ config(materialized='table') }}

SELECT
    DATE_TRUNC(pickup_datetime, MONTH) AS month,
    service_type,
    pickup_borough,
    
    -- Pre-aggregated metrics
    COUNT(*) AS total_trips,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_fare,
    AVG(trip_distance) AS avg_distance,
    SUM(tip_amount) AS total_tips,
    AVG(tip_amount / NULLIF(fare_amount, 0)) AS avg_tip_percentage

FROM {{ ref('fact_trips') }}
GROUP BY month, service_type, pickup_borough
```

**Benefits:**
- ✅ Fast dashboard load times
- ✅ Consistent metrics across organization
- ✅ Reduces compute in BI tool
- ✅ Single source of truth

---

## Part 13: Best Practices Summary

### Project Organization

**Recommended Folder Structure:**

```
dbt_project/
├── models/
│   ├── staging/           # 1:1 with sources
│   │   ├── source_a/
│   │   └── source_b/
│   ├── intermediate/      # Optional: complex logic
│   ├── core/             # Facts and dimensions
│   │   ├── dim_*.sql
│   │   └── fact_*.sql
│   └── marts/            # Business-specific datasets
│       ├── marketing/
│       ├── finance/
│       └── analytics/
├── macros/
├── tests/
├── seeds/
└── snapshots/
```

### Naming Conventions

**Files and Models:**
- Staging: `stg_<source>_<entity>.sql` (e.g., `stg_jaffle_shop_orders.sql`)
- Core dimensions: `dim_<entity>.sql` (e.g., `dim_customers.sql`)
- Core facts: `fact_<entity>.sql` (e.g., `fact_orders.sql`)
- Intermediate: `int_<entity>_<verb>.sql` (e.g., `int_orders_joined.sql`)

**Columns:**
- Use `snake_case`
- Boolean: prefix with `is_` or `has_` (e.g., `is_active`)
- Timestamps: suffix with `_at` (e.g., `created_at`)
- Dates: suffix with `_date` (e.g., `order_date`)

### Model Configuration

**Layer-Specific Configs:**

```yaml
# dbt_project.yml
models:
  my_project:
    staging:
      +materialized: view
      +schema: staging
    
    intermediate:
      +materialized: ephemeral
    
    core:
      +materialized: table
      +schema: core
    
    marts:
      +materialized: table
      +schema: marts
```

### Testing Strategy

**Minimum Tests:**
- All primary keys: `unique` + `not_null`
- All foreign keys: `relationships`
- Categorical columns: `accepted_values`
- Critical metrics: custom range tests

### Performance Optimization

**Tips:**
1. Use incremental models for large tables (> 1M rows)
2. Partition tables by date in warehouse
3. Materialize frequently-queried models as tables
4. Use ephemeral for light transformations
5. Limit CTE depth (complex CTEs → intermediate models)
6. Pre-aggregate in dbt (not BI tool)

---

## Part 14: Key Takeaways

### Analytics Engineering Concepts

1. **Role Definition**:
   - Bridges data engineering and data analysis
   - Owns transformation layer
   - Applies software engineering to analytics

2. **ELT > ETL**:
   - Load raw data first
   - Transform in warehouse using SQL
   - Faster, more flexible, transparent

### dbt Core Concepts

1. **Transformation Tool**:
   - Handles "T" in ELT
   - SQL-based transformations
   - Compiles and executes in warehouse

2. **Software Engineering Practices**:
   - Version control (Git)
   - Testing (data quality)
   - Documentation (auto-generated)
   - CI/CD (deployment)

3. **Project Structure**:
   - Staging layer: Clean raw data
   - Core layer: Facts and dimensions
   - Marts layer: Business-specific datasets

### Dimensional Modeling

1. **Kimball Methodology**:
   - Select business process
   - Declare grain
   - Identify dimensions
   - Identify facts

2. **Star Schema**:
   - Fact tables: Measurements
   - Dimension tables: Context
   - Optimized for analytics

### Production Deployment

1. **Development Workflow**:
   - Develop in dev environment
   - Test with CI
   - Deploy to prod with CD
   - Schedule regular runs

2. **Monitoring**:
   - Test results
   - Job execution times
   - Data freshness
   - Model performance

---

## Additional Resources

### Official Documentation
- **dbt Documentation**: https://docs.getdbt.com
- **dbt Best Practices**: https://docs.getdbt.com/guides/best-practices
- **dbt Packages Hub**: https://hub.getdbt.com
- **dbt Discourse Community**: https://discourse.getdbt.com

### Learning Resources
- **dbt Fundamentals Course** (Free): https://courses.getdbt.com
- **Kimball Dimensional Modeling**: "The Data Warehouse Toolkit" by Ralph Kimball
- **Analytics Engineering Guide**: https://www.getdbt.com/analytics-engineering