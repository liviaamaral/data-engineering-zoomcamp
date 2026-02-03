# Data Engineering Zoomcamp - Module 3 Notes

## Module Overview: Data Warehouse & BigQuery

Module 3 focuses on data warehousing concepts and Google BigQuery, a serverless cloud data warehouse solution. You'll learn the fundamentals of OLAP vs OLTP systems, how to optimize queries using partitioning and clustering, work with external tables, and even explore machine learning capabilities within BigQuery.

---

## Part 1: Introduction to Data Warehousing

### What is a Data Warehouse?

A **Data Warehouse** is a centralized repository designed for reporting and data analysis. It serves as the core of business intelligence (BI) systems by consolidating data from multiple sources into a single, structured location optimized for analytical queries.

**Key Characteristics:**
- Subject-oriented: Organized around key business subjects (sales, customers, products)
- Integrated: Combines data from multiple sources with consistent formats
- Non-volatile: Historical data is preserved and not overwritten
- Time-variant: Tracks changes over time for trend analysis

**Data Warehouse Architecture:**

```
Data Sources (OLTP) → Staging Area → Data Warehouse → Data Marts → BI/Analytics
     ↓                      ↓              ↓              ↓            ↓
Transactional DBs     ETL Process    Optimized      Department-   Dashboards
Flat Files            Cleansing      Storage        Specific      Reports
APIs                  Transform      Denormalized   Subsets       Queries
```

### OLTP vs OLAP

Understanding the difference between Online Transaction Processing (OLTP) and Online Analytical Processing (OLAP) is fundamental to data engineering.

**OLTP (Online Transaction Processing):**
- **Purpose**: Backend services and transactional operations
- **Queries**: Simple, fast INSERT/UPDATE/DELETE operations
- **Data Volume**: Small, focused transactions
- **Users**: Large number of concurrent users
- **Data Structure**: Highly normalized to reduce redundancy
- **Response Time**: Milliseconds
- **Examples**: 
  - Online shopping cart operations
  - Banking transactions
  - Order processing systems
  - Inventory management

**OLAP (Online Analytical Processing):**
- **Purpose**: Analytics, reporting, and business intelligence
- **Queries**: Complex SELECT queries with aggregations and joins
- **Data Volume**: Large datasets spanning historical data
- **Users**: Smaller number of analysts and decision-makers
- **Data Structure**: Denormalized for query performance
- **Response Time**: Seconds to minutes
- **Examples**:
  - Sales trend analysis
  - Executive dashboards
  - Customer behavior analytics
  - Financial forecasting

**Comparison Table:**

| Feature | OLTP | OLAP |
|---------|------|------|
| **Workload** | Transactional | Analytical |
| **Operations** | INSERT, UPDATE, DELETE | SELECT (with aggregations) |
| **Database Design** | Normalized | Denormalized |
| **Data Volume per Query** | Small | Large |
| **Query Complexity** | Simple | Complex |
| **Update Frequency** | Real-time, continuous | Periodic batch updates |
| **Performance Priority** | Fast writes | Fast reads |
| **Examples** | MySQL, PostgreSQL | BigQuery, Redshift, Snowflake |

---

## Part 2: Understanding Data Storage Concepts

### Data Warehouse vs Data Lake vs Data Lakehouse

**Data Warehouse:**
- **Metaphor**: A well-organized library with cataloged books
- **Structure**: Highly structured, schema-on-write
- **Data Type**: Processed, cleaned, structured data
- **Use Case**: Business intelligence, reporting, analytics
- **Cost**: Higher due to processing and storage optimization
- **Examples**: Google BigQuery, Amazon Redshift, Azure Synapse Analytics

**Data Lake:**
- **Metaphor**: A vast storage room with boxes requiring exploration
- **Structure**: Unstructured or semi-structured, schema-on-read
- **Data Type**: Raw data in native format (CSV, JSON, Parquet, images, videos)
- **Use Case**: Big data processing, machine learning, data science exploration
- **Cost**: Lower storage costs, pay for compute when processing
- **Examples**: Google Cloud Storage (GCS), Amazon S3, Azure Data Lake Storage

**Data Lakehouse:**
- **Metaphor**: Hybrid combining library organization with storage room capacity
- **Structure**: Combines structured warehouse with flexible lake storage
- **Data Type**: Both raw and processed data with metadata layers
- **Use Case**: Unified analytics platform for BI and ML
- **Cost**: Balanced approach optimizing storage and query performance
- **Examples**: Databricks Delta Lake, Apache Iceberg, Apache Hudi

**Data Mart:**
- **Metaphor**: A specialized section of the library for specific departments
- **Structure**: Subset of data warehouse focused on specific business area
- **Data Type**: Department-specific aggregated data
- **Use Case**: Team-specific reporting (Sales, Marketing, Finance)
- **Examples**: Sales data mart, Customer analytics mart

---

## Part 3: Introduction to Google BigQuery

### What is BigQuery?

**BigQuery** is Google Cloud Platform's fully managed, serverless data warehouse solution designed for analyzing massive datasets using SQL queries.

**Core Features:**

1. **Serverless Architecture**
   - No infrastructure to provision or manage
   - No database software to install
   - Automatically scales from gigabytes to petabytes
   - High availability built-in

2. **Separation of Compute and Storage**
   - Storage and compute are independently scalable
   - Pay only for what you use
   - Flexibility to optimize costs
   - Store data cheaply, pay for queries when run

3. **Built-in Advanced Features**
   - **BigQuery ML**: Create and train ML models using SQL
   - **Geospatial Analysis**: GIS functions for location data
   - **Business Intelligence**: Native integration with BI tools
   - **Streaming Inserts**: Real-time data ingestion

4. **Columnar Storage**
   - Data stored by column rather than row
   - Optimized for analytical queries
   - Read only columns needed for query
   - Significantly faster aggregations

5. **Automatic Query Optimization**
   - Query execution is optimized automatically
   - Parallel processing across distributed nodes
   - Caching of query results
   - Smart query plan generation

### BigQuery Architecture

Understanding BigQuery's internal architecture helps optimize query performance:

**Four Core Components:**

1. **Colossus** (Storage Layer)
   - Google's distributed file system
   - Stores data in columnar format
   - Cheap, durable storage
   - Separated from compute cluster
   - Enables independent scaling

2. **Jupiter** (Network)
   - Google's high-speed internal network
   - Connects Colossus to compute engines
   - 1 Petabit/second bandwidth
   - Ensures low latency data access
   - Enables fast data transfers

3. **Dremel** (Query Engine)
   - Executes SQL queries
   - Divides queries into tree structure
   - Distributes execution across thousands of nodes
   - Each node processes subset of data
   - Aggregates results back up the tree
   - Massively parallel processing

4. **Borg** (Orchestration)
   - Google's cluster management system
   - Handles resource allocation
   - Manages query execution
   - Ensures high availability
   - Coordinates everything behind the scenes

**How a Query Executes:**

```
User submits SQL query
        ↓
Borg receives query and allocates resources
        ↓
Dremel breaks query into execution tree
        ↓
Query distributed across thousands of workers
        ↓
Each worker reads data from Colossus via Jupiter
        ↓
Workers process their data chunks in parallel
        ↓
Results aggregated back up the tree
        ↓
Final results returned to user
```

### BigQuery Pricing

BigQuery offers two pricing models:

**1. On-Demand Pricing**
- **Cost**: $5 per TB of data processed
- **Free Tier**: First 1 TB per month is free
- **Best For**: 
  - Small to medium workloads
  - Variable query patterns
  - Development and testing
  - Unpredictable usage
- **Billing**: Pay only for queries you run
- **No commitments**: Flexible scaling

**2. Flat-Rate Pricing**
- **Cost**: $2,000/month for 100 slots minimum
- **Slots**: Units of computational capacity
- **Best For**: 
  - Heavy users (>200 TB/month)
  - Predictable workloads
  - Cost control and budgeting
  - Enterprise deployments
- **Billing**: Fixed monthly cost regardless of usage
- **Commitments**: Monthly or annual contracts

**Storage Pricing:**
- **Active Storage**: $0.020 per GB/month
- **Long-term Storage**: $0.010 per GB/month (tables not edited for 90 days)

**Cost Optimization Tips:**
1. Avoid `SELECT *` - query only needed columns
2. Use partitioning and clustering
3. Leverage cached query results (free, valid for 24 hours)
4. Preview data with `LIMIT` during development
5. Use query cost estimator before running
6. Set maximum bytes billed for cost control
7. Monitor usage with BigQuery audit logs

---

## Part 4: Working with Tables in BigQuery

### Table Types

BigQuery supports two main table types:

**1. External Tables**

External tables reference data stored outside BigQuery (e.g., in Google Cloud Storage) without importing it.

**Characteristics:**
- Data remains in external storage (GCS, Cloud Bigtable, Google Drive)
- No storage costs in BigQuery
- Schema can be auto-detected or manually defined
- Query performance may be slower than native tables
- Cannot estimate table size before querying
- No table metadata (row count, size) available

**When to Use:**
- Data changes frequently in source system
- Want to avoid data duplication
- Exploratory analysis before full import
- Cost-sensitive scenarios
- One-time or infrequent queries

**Creating an External Table:**

```sql
-- Create external table from GCS
CREATE OR REPLACE EXTERNAL TABLE `project.dataset.external_yellow_taxi`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bucket_name/yellow_taxi/2024/*.parquet']
);

-- With CSV format
CREATE OR REPLACE EXTERNAL TABLE `project.dataset.external_green_taxi`
OPTIONS (
  format = 'CSV',
  uris = ['gs://bucket_name/green_taxi_2024-*.csv.gz'],
  skip_leading_rows = 1
);
```

**2. Materialized Tables (Native BigQuery Tables)**

These are traditional BigQuery tables where data is stored within BigQuery.

**Characteristics:**
- Data copied into BigQuery storage
- Charged for storage
- Faster query performance
- Full metadata available (row count, size, schema)
- Can be partitioned and clustered
- Supports table-level optimizations

**When to Use:**
- Frequent queries on the same data
- Need optimal query performance
- Require partitioning or clustering
- Production workloads
- Data quality checks and constraints

**Creating a Materialized Table:**

```sql
-- Create from external table
CREATE OR REPLACE TABLE `project.dataset.yellow_taxi_materialized` AS
SELECT * FROM `project.dataset.external_yellow_taxi`;

-- Create with specific schema
CREATE OR REPLACE TABLE `project.dataset.trips` (
  trip_id STRING,
  pickup_datetime TIMESTAMP,
  dropoff_datetime TIMESTAMP,
  passenger_count INT64,
  trip_distance FLOAT64,
  fare_amount FLOAT64
);
```

### Key Differences: External vs Materialized

| Feature | External Table | Materialized Table |
|---------|---------------|-------------------|
| **Data Location** | External (GCS, Drive, etc.) | BigQuery storage |
| **Storage Cost** | $0 in BigQuery | Standard BigQuery storage rates |
| **Query Performance** | Slower (read from external) | Faster (optimized storage) |
| **Metadata** | Limited | Full (row count, size, etc.) |
| **Partitioning** | Not supported | Supported |
| **Clustering** | Not supported | Supported |
| **Data Freshness** | Always current (if source updates) | Requires refresh |
| **Setup Time** | Instant | Requires data import |
| **Best Use** | Infrequent queries, exploration | Production, frequent queries |

---

## Part 5: Columnar Storage

### Row-Oriented vs Column-Oriented Storage

**Row-Oriented Storage (OLTP)**

Data is stored row by row, like a CSV file:

```
Row 1: John, 25, Engineer, 75000
Row 2: Mary, 30, Manager, 85000
Row 3: Bob, 28, Analyst, 65000
```

**Advantages:**
- Fast for writing entire records
- Efficient for retrieving complete rows
- Good for OLTP operations (INSERT, UPDATE, DELETE)

**Disadvantages:**
- Slow for analytics that need specific columns
- Must read entire row even if only need one column
- Poor compression ratios

**Column-Oriented Storage (OLAP)**

Data is stored column by column:

```
Name column: John, Mary, Bob
Age column: 25, 30, 28
Role column: Engineer, Manager, Analyst
Salary column: 75000, 85000, 65000
```

**Advantages:**
- Fast for analytics queries
- Read only columns needed for query
- Better compression (similar data types together)
- Efficient aggregations (SUM, AVG, COUNT)

**Disadvantages:**
- Slower for writing individual records
- Not optimal for retrieving entire rows

**BigQuery Example:**

```sql
-- Query 1: Only reading one column
SELECT PULocationID FROM `project.dataset.yellow_taxi`;
-- Estimated bytes: 6.4 MB

-- Query 2: Reading two columns
SELECT PULocationID, DOLocationID FROM `project.dataset.yellow_taxi`;
-- Estimated bytes: 12.8 MB (exactly double!)
```

**Key Insight**: BigQuery only scans the columns you request, which is why selecting specific columns is much cheaper than `SELECT *`.

---

## Part 6: Partitioning in BigQuery

### What is Partitioning?

**Partitioning** divides a large table into smaller segments based on a specific column, making queries faster and cheaper by scanning only relevant partitions.

**Analogy**: Instead of searching through an entire filing cabinet, you go directly to the drawer labeled with the date range you need.

### Partition Types

BigQuery supports three partition types:

**1. Time-Unit Column Partitioning**

Partition based on a TIMESTAMP, DATE, or DATETIME column.

```sql
-- Partition by DATE column
CREATE OR REPLACE TABLE `project.dataset.yellow_taxi_partitioned`
PARTITION BY DATE(pickup_datetime)
AS SELECT * FROM `project.dataset.yellow_taxi_materialized`;
```

**Granularity Options:**
- **HOUR**: For very high-frequency data
- **DAY**: Default, most common
- **MONTH**: For monthly reporting
- **YEAR**: For annual analysis

**2. Ingestion Time Partitioning**

Partition based on when data was loaded into BigQuery.

```sql
CREATE OR REPLACE TABLE `project.dataset.taxi_ingestion_partitioned`
PARTITION BY _PARTITIONDATE
AS SELECT * FROM `project.dataset.yellow_taxi`;
```

**Note**: Uses pseudo-column `_PARTITIONDATE` automatically created by BigQuery.

**3. Integer Range Partitioning**

Partition based on an integer column.

```sql
CREATE OR REPLACE TABLE `project.dataset.taxi_by_location`
PARTITION BY RANGE_BUCKET(PULocationID, GENERATE_ARRAY(0, 300, 10))
AS SELECT * FROM `project.dataset.yellow_taxi`;
```

**Use Cases**: Customer IDs, product categories, geographical zones

### Partition Benefits

**Performance Improvement:**

```sql
-- Non-partitioned table query
SELECT COUNT(*) 
FROM `project.dataset.yellow_taxi_non_partitioned`
WHERE DATE(pickup_datetime) = '2024-06-01';
-- Scans: 1.6 GB (entire table)

-- Partitioned table query
SELECT COUNT(*) 
FROM `project.dataset.yellow_taxi_partitioned`
WHERE DATE(pickup_datetime) = '2024-06-01';
-- Scans: 45 MB (only one partition!)
```

**Cost Savings**: Reduced data scanned = lower query costs

**Real Example from Homework:**
- Non-partitioned query: 647 MB scanned
- Partitioned query: 23 MB scanned
- **Cost reduction: 96%**

### Partition Best Practices

1. **Choose the Right Column**:
   - Use columns frequently filtered in WHERE clauses
   - Typically date/timestamp columns
   - Should have reasonable cardinality

2. **Partition Limits**:
   - Maximum 4,000 partitions per table
   - Plan partition granularity accordingly
   - Use MONTH or YEAR partitioning for long historical data

3. **Partition Pruning**:
   ```sql
   -- Good: Partition pruning works
   WHERE DATE(pickup_datetime) >= '2024-01-01'
   
   -- Bad: Full table scan
   WHERE EXTRACT(YEAR FROM pickup_datetime) = 2024
   ```

4. **Require Partition Filter** (for cost control):
   ```sql
   ALTER TABLE `project.dataset.yellow_taxi_partitioned`
   SET OPTIONS (
     require_partition_filter = TRUE
   );
   ```

---

## Part 7: Clustering in BigQuery

### What is Clustering?

**Clustering** sorts data within partitions (or the entire table) based on one or more columns, improving query performance for filters and joins on those columns.

**Analogy**: Like alphabetizing books within each section of a library - makes finding specific books much faster.

### How Clustering Works

When you cluster a table, BigQuery:
1. Sorts data by the cluster columns
2. Groups similar values together in storage blocks
3. Tracks which values are in which blocks
4. Skips blocks that don't contain relevant values during queries

### Creating Clustered Tables

```sql
-- Partition by date, cluster by location
CREATE OR REPLACE TABLE `project.dataset.yellow_taxi_partitioned_clustered`
PARTITION BY DATE(pickup_datetime)
CLUSTER BY VendorID, PULocationID
AS SELECT * FROM `project.dataset.yellow_taxi`;
```

**Clustering Rules:**
- Maximum 4 clustering columns
- Order matters (cluster by most filtered columns first)
- Can cluster without partitioning
- Clustering happens automatically as data is written

### Partitioning vs Clustering

**When to Use Partitioning:**
- Filter or aggregate on a specific column (usually date)
- Data spans a clear time range
- Need partition-level management (expiration, deletion)
- Want predictable costs (know partition sizes)

**When to Use Clustering:**
- Filter on multiple columns
- Column has high cardinality (many unique values)
- Query patterns vary
- Don't have a natural partition column

**When to Use Both:**
- Large tables with both temporal and categorical filters
- Best practice for production tables
- Example: Partition by date, cluster by user_id and category

### Performance Comparison

Real-world example from Module 3:

```sql
-- Non-partitioned, non-clustered table
SELECT COUNT(*) FROM `project.dataset.yellow_taxi`
WHERE DATE(pickup_datetime) BETWEEN '2024-01-01' AND '2024-01-31'
  AND VendorID = 1;
-- Scans: 310 MB

-- Partitioned by date only
SELECT COUNT(*) FROM `project.dataset.yellow_taxi_partitioned`
WHERE DATE(pickup_datetime) BETWEEN '2024-01-01' AND '2024-01-31'
  AND VendorID = 1;
-- Scans: 45 MB

-- Partitioned by date AND clustered by VendorID
SELECT COUNT(*) FROM `project.dataset.yellow_taxi_partitioned_clustered`
WHERE DATE(pickup_datetime) BETWEEN '2024-01-01' AND '2024-01-31'
  AND VendorID = 1;
-- Scans: 26 MB (58% reduction from partition only!)
```

### Clustering Best Practices

1. **Choose Cluster Columns Wisely**:
   - Columns used in WHERE clauses
   - Columns used in JOIN conditions
   - High-cardinality columns (many distinct values)
   - Put most frequently filtered columns first

2. **Limit Cluster Columns**:
   - Maximum 4 columns
   - More isn't always better
   - Consider query patterns

3. **Monitor Clustering Quality**:
   ```sql
   -- Check if table is well-clustered
   SELECT 
     table_name,
     total_rows,
     total_partitions,
     clustering_ordinal_position,
     clustering_field
   FROM `project.dataset.INFORMATION_SCHEMA.COLUMNS`
   WHERE table_name = 'yellow_taxi_partitioned_clustered';
   ```

4. **Automatic Re-clustering**:
   - BigQuery automatically maintains clustering
   - No manual maintenance required
   - Happens in background as data is modified

5. **When NOT to Cluster**:
   - Small tables (< 1 GB) - overhead not worth it
   - Tables with few distinct values in cluster columns
   - Write-heavy tables where clustering overhead impacts performance

---

## Part 8: Loading Data into BigQuery

### Methods for Loading Data

BigQuery supports multiple ways to ingest data:

**1. Loading from Google Cloud Storage (GCS)**

Most common method for bulk data loading.

```sql
-- Load from single file
LOAD DATA OVERWRITE `project.dataset.trips`
FROM FILES (
  format = 'PARQUET',
  uris = ['gs://bucket_name/data/trips.parquet']
);

-- Load from multiple files with pattern matching
CREATE OR REPLACE TABLE `project.dataset.yellow_taxi_2024`
AS SELECT * FROM 
EXTERNAL_QUERY(
  'gs://nyc-tlc/yellow_taxi/2024/*.parquet',
  format => 'PARQUET'
);
```

**Load Job Configuration:**
```sql
-- Using bq command-line tool
bq load \
  --source_format=PARQUET \
  --autodetect \
  project:dataset.yellow_taxi \
  gs://bucket_name/yellow_taxi_*.parquet
```

**2. Loading from Local Files**

For development and small datasets.

```bash
# Using bq CLI
bq load \
  --source_format=CSV \
  --skip_leading_rows=1 \
  --autodetect \
  project:dataset.trips \
  ./local_trips.csv
```

**3. Streaming Inserts**

For real-time data ingestion.

```python
from google.cloud import bigquery

client = bigquery.Client()
table_id = "project.dataset.trips"

rows_to_insert = [
    {"trip_id": "123", "fare_amount": 25.50},
    {"trip_id": "124", "fare_amount": 30.00}
]

errors = client.insert_rows_json(table_id, rows_to_insert)
if errors:
    print(f"Errors: {errors}")
```

**Note**: Streaming inserts have costs ($0.010 per 200 MB) and are billed separately.

**4. Data Transfer Service**

Automated, scheduled data transfers from SaaS applications.

- Google Ads
- YouTube
- Google Play
- 3rd party sources (Amazon S3, Salesforce, etc.)

**5. BigQuery Data Transfer API**

Programmatic bulk data transfers.

```python
from google.cloud import bigquery_datatransfer

client = bigquery_datatransfer.DataTransferServiceClient()

# Configure transfer from GCS
transfer_config = bigquery_datatransfer.TransferConfig(
    destination_dataset_id="my_dataset",
    display_name="GCS Transfer",
    data_source_id="google_cloud_storage",
    params={
        "data_path_template": "gs://bucket/path/*.csv",
        "destination_table_name_template": "my_table",
        "file_format": "CSV"
    }
)
```

### Loading Best Practices

1. **Use Appropriate File Formats**:
   - **Parquet**: Best for analytics, columnar, compressed
   - **Avro**: Good for row-based, supports schema evolution
   - **CSV**: Simple but least efficient, largest size
   - **JSON**: Flexible but verbose

2. **Optimize File Size**:
   - Ideal: 100 MB - 5 GB per file
   - Too small: Poor parallelization
   - Too large: Harder to retry on failures

3. **Enable Schema Auto-detection** (for development):
   ```sql
   CREATE OR REPLACE TABLE `project.dataset.trips`
   AS SELECT * FROM
   EXTERNAL_QUERY(
     'gs://bucket/trips.parquet',
     format => 'PARQUET',
     autodetect => TRUE
   );
   ```

4. **Set Write Disposition**:
   - `WRITE_TRUNCATE`: Overwrite existing table
   - `WRITE_APPEND`: Add to existing table
   - `WRITE_EMPTY`: Only if table is empty

5. **Monitor Load Jobs**:
   ```sql
   SELECT
     job_id,
     state,
     error_result,
     total_bytes_processed
   FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
   WHERE job_type = 'LOAD'
   ORDER BY creation_time DESC
   LIMIT 10;
   ```

---

## Part 9: BigQuery Best Practices & Optimization

### Query Optimization Techniques

**1. Select Only Required Columns**

```sql
-- Bad: Scans entire table
SELECT * FROM `project.dataset.yellow_taxi`;
-- Scans: 2.5 GB

-- Good: Scans only needed columns
SELECT pickup_datetime, trip_distance, fare_amount 
FROM `project.dataset.yellow_taxi`;
-- Scans: 450 MB (82% reduction!)
```

**2. Filter Early and Often**

```sql
-- Bad: Filter after aggregation
SELECT vendor_id, SUM(fare_amount)
FROM (
  SELECT * FROM `project.dataset.yellow_taxi`
)
WHERE pickup_datetime >= '2024-01-01'
GROUP BY vendor_id;

-- Good: Filter before aggregation
SELECT vendor_id, SUM(fare_amount)
FROM `project.dataset.yellow_taxi`
WHERE pickup_datetime >= '2024-01-01'
GROUP BY vendor_id;
```

**3. Use Partitioning Wisely**

```sql
-- Bad: Partition filter doesn't prune
SELECT COUNT(*)
FROM `project.dataset.yellow_taxi_partitioned`
WHERE EXTRACT(MONTH FROM pickup_datetime) = 6;
-- Still scans all partitions!

-- Good: Partition pruning works
SELECT COUNT(*)
FROM `project.dataset.yellow_taxi_partitioned`
WHERE pickup_datetime >= '2024-06-01' 
  AND pickup_datetime < '2024-07-01';
-- Only scans June partition
```

**4. Leverage Caching**

```sql
-- First run: Processes data
SELECT COUNT(*) FROM `project.dataset.yellow_taxi`;
-- Scans: 1.5 GB, Duration: 3.2 sec

-- Second run (within 24 hours): Uses cache
SELECT COUNT(*) FROM `project.dataset.yellow_taxi`;
-- Scans: 0 GB (cached!), Duration: 0.1 sec, Cost: $0
```

**Note**: Cached results are valid for 24 hours and are free!

**5. Use LIMIT Wisely**

```sql
-- LIMIT doesn't reduce scanned data
SELECT * FROM `project.dataset.yellow_taxi` LIMIT 100;
-- Still scans: 2.5 GB (full table!)

-- Better: Combine with partitioning
SELECT * 
FROM `project.dataset.yellow_taxi_partitioned`
WHERE pickup_datetime >= '2024-01-01'
  AND pickup_datetime < '2024-01-02'
LIMIT 100;
-- Scans: Only 1 day's partition
```

**6. Avoid Self-Joins When Possible**

```sql
-- Bad: Self-join
SELECT t1.*, t2.fare_amount
FROM `project.dataset.trips` t1
JOIN `project.dataset.trips` t2
  ON t1.trip_id = t2.trip_id;

-- Good: Window function
SELECT 
  *,
  LAST_VALUE(fare_amount) OVER (
    PARTITION BY trip_id 
    ORDER BY pickup_datetime
  ) as last_fare
FROM `project.dataset.trips`;
```

**7. Use Approximate Aggregation for Large Datasets**

```sql
-- Exact count (slower, more expensive)
SELECT COUNT(DISTINCT user_id) FROM `project.dataset.events`;
-- Scans: 10 GB

-- Approximate count (faster, cheaper, 98%+ accurate)
SELECT APPROX_COUNT_DISTINCT(user_id) FROM `project.dataset.events`;
-- Scans: 10 GB but processes faster
```

**8. Denormalize Data for Analytics**

```sql
-- Bad: Normalized, requires joins
SELECT o.order_id, c.customer_name, p.product_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id;

-- Good: Denormalized, pre-joined
SELECT order_id, customer_name, product_name
FROM orders_denormalized;
```

**Note**: BigQuery is optimized for storage (cheap) over compute, so denormalization usually improves performance.

### Cost Control Strategies

**1. Set Maximum Bytes Billed**

```sql
-- Set query cost limit
SET @@query_max_bytes_billed = 1099511627776; -- 1 TB limit

SELECT * FROM `project.dataset.large_table`;
-- Query fails if would process > 1 TB
```

**2. Use Query Dry Run**

```bash
# Check query cost before running
bq query --dry_run --use_legacy_sql=false \
  'SELECT * FROM `project.dataset.yellow_taxi`'
# Output: Query will process 2.5 GB
```

**3. Create Cost-Effective Views**

```sql
-- Materialized view (cached, faster, uses storage)
CREATE MATERIALIZED VIEW `project.dataset.daily_fares` AS
SELECT 
  DATE(pickup_datetime) as trip_date,
  SUM(fare_amount) as total_fares
FROM `project.dataset.yellow_taxi`
GROUP BY trip_date;

-- Querying the materialized view is cheaper
SELECT * FROM `project.dataset.daily_fares`
WHERE trip_date = '2024-06-01';
-- Scans: Only the materialized view (much smaller!)
```

**4. Monitor Query Costs**

```sql
-- View job costs
SELECT
  user_email,
  job_id,
  total_bytes_processed,
  (total_bytes_processed / 1099511627776) * 5 as estimated_cost_usd
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE DATE(creation_time) = CURRENT_DATE()
ORDER BY total_bytes_processed DESC;
```

---

## Part 10: BigQuery ML (Machine Learning)

### Introduction to BigQuery ML

**BigQuery ML (BQML)** enables data analysts to create and execute machine learning models using standard SQL queries, without needing to move data out of BigQuery or learn Python/R.

**Supported Model Types:**
- Linear Regression
- Logistic Regression
- K-means Clustering
- Time Series (ARIMA)
- Deep Neural Networks (DNN)
- Boosted Trees
- Random Forest
- AutoML Tables
- TensorFlow models (imported)

### Creating a Linear Regression Model

**Goal**: Predict taxi tip amounts based on trip characteristics

**Step 1: Prepare Training Data**

```sql
-- Create feature table
CREATE OR REPLACE TABLE `project.dataset.yellow_tripdata_ml` AS
SELECT
  tip_amount,
  fare_amount,
  trip_distance,
  PULocationID,
  DOLocationID,
  passenger_count,
  EXTRACT(HOUR FROM pickup_datetime) as pickup_hour,
  EXTRACT(DAYOFWEEK FROM pickup_datetime) as pickup_day
FROM `project.dataset.yellow_taxi_partitioned`
WHERE 
  tip_amount IS NOT NULL
  AND fare_amount > 0
  AND trip_distance > 0
  AND pickup_datetime >= '2024-01-01'
  AND pickup_datetime < '2024-03-01';
```

**Step 2: Create and Train Model**

```sql
CREATE OR REPLACE MODEL `project.dataset.tip_prediction_model`
OPTIONS(
  model_type='linear_reg',
  input_label_cols=['tip_amount'],
  data_split_method='AUTO_SPLIT' -- 80/20 train/test split
) AS
SELECT
  tip_amount,
  fare_amount,
  trip_distance,
  PULocationID,
  DOLocationID,
  passenger_count,
  pickup_hour,
  pickup_day
FROM `project.dataset.yellow_tripdata_ml`
WHERE tip_amount IS NOT NULL;
```

**Step 3: Evaluate Model**

```sql
-- View training statistics
SELECT * FROM ML.TRAINING_INFO(MODEL `project.dataset.tip_prediction_model`);

-- Evaluate model performance
SELECT
  mean_absolute_error,
  mean_squared_error,
  r2_score
FROM ML.EVALUATE(MODEL `project.dataset.tip_prediction_model`);
```

**Example Output:**
```
mean_absolute_error: 0.85
mean_squared_error: 2.34
r2_score: 0.72
```

**Step 4: Make Predictions**

```sql
-- Predict tips for new trips
SELECT
  *,
  predicted_tip_amount,
  tip_amount as actual_tip_amount,
  ABS(predicted_tip_amount - tip_amount) as prediction_error
FROM ML.PREDICT(
  MODEL `project.dataset.tip_prediction_model`,
  (
    SELECT
      tip_amount,
      fare_amount,
      trip_distance,
      PULocationID,
      DOLocationID,
      passenger_count,
      pickup_hour,
      pickup_day
    FROM `project.dataset.yellow_tripdata_ml`
    WHERE pickup_datetime >= '2024-03-01'
    LIMIT 100
  )
);
```

### Hyperparameter Tuning

Optimize model performance by testing different hyperparameters:

```sql
CREATE OR REPLACE MODEL `project.dataset.tip_hyperparam_model`
OPTIONS(
  model_type='linear_reg',
  input_label_cols=['tip_amount'],
  data_split_method='AUTO_SPLIT',
  num_trials=5,
  max_parallel_trials=2,
  l1_reg=hparam_range(0, 20),
  l2_reg=hparam_candidates([0, 0.1, 1, 10])
) AS
SELECT * FROM `project.dataset.yellow_tripdata_ml`
WHERE tip_amount IS NOT NULL;
```

**Hyperparameters:**
- `num_trials`: Number of tuning iterations
- `max_parallel_trials`: Concurrent trials
- `l1_reg`: L1 regularization range (prevents overfitting)
- `l2_reg`: L2 regularization candidates

### Model Export and Deployment

**Export Model to GCS:**

```sql
EXPORT MODEL `project.dataset.tip_prediction_model`
OPTIONS(
  uri='gs://bucket_name/models/tip_prediction_model'
);
```

**Deploy with TensorFlow Serving:**

```bash
# Pull TensorFlow Serving image
docker pull tensorflow/serving

# Run model server
docker run -p 8501:8501 \
  --mount type=bind,source=/path/to/model,target=/models/tip_model \
  -e MODEL_NAME=tip_model \
  -t tensorflow/serving
```

**Make predictions via REST API:**

```bash
curl -X POST http://localhost:8501/v1/models/tip_model:predict \
  -H 'Content-Type: application/json' \
  -d '{
    "instances": [
      {
        "fare_amount": 15.5,
        "trip_distance": 5.2,
        "passenger_count": 1
      }
    ]
  }'
```

### BigQuery ML Best Practices

1. **Feature Engineering**:
   - Create meaningful features from raw data
   - Extract temporal features (hour, day, month)
   - Normalize numeric features
   - Encode categorical variables

2. **Data Splitting**:
   - Use `AUTO_SPLIT` for automatic 80/20 split
   - Or manually split with `data_split_col`

3. **Handle Null Values**:
   ```sql
   SELECT * FROM table
   WHERE target_column IS NOT NULL;
   ```

4. **Model Selection**:
   - Linear/Logistic Regression: Fast, interpretable
   - Boosted Trees: Better accuracy, slower training
   - AutoML: Best performance, highest cost

5. **Evaluation Metrics**:
   - **Regression**: R², MAE, RMSE
   - **Classification**: Accuracy, Precision, Recall, AUC-ROC

## Part 11: Key Takeaways

### Data Warehousing Concepts

1. **OLTP vs OLAP**:
   - OLTP: Transactional systems, row-oriented, normalized
   - OLAP: Analytical systems, columnar, denormalized
   - Different tools for different purposes

2. **Storage Solutions**:
   - Data Warehouse: Structured, optimized for BI
   - Data Lake: Raw, flexible, cost-effective
   - Data Lakehouse: Hybrid approach combining both

### BigQuery Fundamentals

1. **Architecture**:
   - Serverless, fully managed
   - Separation of compute and storage
   - Columnar storage optimized for analytics
   - Automatic scaling and optimization

2. **Pricing**:
   - On-demand: $5/TB processed
   - Flat-rate: $2,000/month for 100 slots
   - Storage: Separate charges
   - Free tier: 1 TB/month query processing

### Performance Optimization

1. **Partitioning**:
   - Divides tables into segments
   - Reduces data scanned
   - Based on time-unit, ingestion time, or integer range
   - Up to 4,000 partitions per table

2. **Clustering**:
   - Sorts data within partitions
   - Improves filter and join performance
   - Up to 4 clustering columns
   - Automatic maintenance

3. **Query Best Practices**:
   - Select only required columns
   - Filter early and often
   - Use partitioning and clustering
   - Leverage cached results
   - Denormalize for analytics

### BigQuery ML

1. **Capabilities**:
   - Create ML models using SQL
   - No data export needed
   - Multiple model types supported
   - Hyperparameter tuning built-in

2. **Model Deployment**:
   - Export to GCS
   - Deploy with TensorFlow Serving
   - Serve predictions via API

### Real-World Applications

1. **Data Pipeline**:
   ```
   Source Data → GCS → External Table → Materialized Table
        ↓
   Partition & Cluster → Optimize Queries → Build ML Models
   ```

2. **Cost Optimization**:
   - Partition by date for time-series data
   - Cluster by frequently filtered columns
   - Monitor query costs
   - Use materialized views for repeated queries

3. **Production Deployment**:
   - Automate with orchestration tools
   - Implement monitoring and alerting
   - Use scheduled queries for regular updates
   - Set up data quality checks

---

## Additional Resources

### Official Documentation
- **BigQuery Documentation**: https://cloud.google.com/bigquery/docs
- **BigQuery Pricing**: https://cloud.google.com/bigquery/pricing
- **BigQuery ML**: https://cloud.google.com/bigquery-ml/docs
- **SQL Reference**: https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax

### Data Engineering Zoomcamp
- [Course GitHub](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- [YouTube Playlist](https://www.youtube.com/playlist?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
