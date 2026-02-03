create schema `data-engineering-zoomcamp-hmw3.ny_taxi`
options (
  location = 'US'
);

-- Create external table
create or replace external table `data-engineering-zoomcamp-hmw3.ny_taxi.yellow_taxi_external`
options (
  format = 'PARQUET',  -- or 'CSV' depending on your file format
  uris = ['gs://bucket-hmw3/*.parquet']  -- adjust path as needed
);

-- Create regular table (no partitioning or clustering)
create or replace table `data-engineering-zoomcamp-hmw3.ny_taxi.yellow_taxi_regular` AS
select * from `data-engineering-zoomcamp-hmw3.ny_taxi.yellow_taxi_external`;

-- What is count of records for the 2024 Yellow Taxi Data?
select count(*) from `data-engineering-zoomcamp-hmw3.ny_taxi.yellow_taxi_regular`;

-- Select distinct number of PULocationIDs from both tables
select count(distinct(PULocationID)) from `data-engineering-zoomcamp-hmw3.ny_taxi.yellow_taxi_external`;
select count(distinct(PULocationID)) from `data-engineering-zoomcamp-hmw3.ny_taxi.yellow_taxi_regular`;

-- Select number of PULocationID from BigQuery table, and then PULocationID and DOLocationID
select PULocationID from `data-engineering-zoomcamp-hmw3.ny_taxi.yellow_taxi_regular`;
select PULocationID, DOLocationID from `data-engineering-zoomcamp-hmw3.ny_taxi.yellow_taxi_regular`;

-- How many records have a fare_amount of 0?
select count(*) from `data-engineering-zoomcamp-hmw3.ny_taxi.yellow_taxi_regular`
where fare_amount = 0;

-- Table optimization when always filtering based on dropoff time and ordering by VendorID
create or replace table `data-engineering-zoomcamp-hmw3.ny_taxi.yellow_taxi_regular_optimized`
partition by date(tpep_dropoff_datetime)
cluster by VendorID
as select * from `data-engineering-zoomcamp-hmw3.ny_taxi.yellow_taxi_regular`;

-- Retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)
select distinct(VendorID) from `data-engineering-zoomcamp-hmw3.ny_taxi.yellow_taxi_regular`
where date(tpep_dropoff_datetime) between '2024-03-01' and '2024-03-15';

select distinct(VendorID) from `data-engineering-zoomcamp-hmw3.ny_taxi.yellow_taxi_regular_optimized`
where date(tpep_dropoff_datetime) between '2024-03-01' and '2024-03-15';


-- Write a `SELECT count(*)` query FROM the materialized table you created.
select count(*) from `data-engineering-zoomcamp-hmw3.ny_taxi.yellow_taxi_regular`;
