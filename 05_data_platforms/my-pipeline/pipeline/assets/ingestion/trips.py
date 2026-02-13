"""@bruin

# TODO: Set the asset name (recommended pattern: schema.asset_name).
# - Convention in this module: use an `ingestion.` schema for raw ingestion tables.
name: ingestion.trips

# TODO: Set the asset type.
# Docs: https://getbruin.com/docs/bruin/assets/python
type: python

# TODO: Pick a Python image version (Bruin runs Python in isolated environments).
# Example: python:3.11
image: python:3.11

# Connection for materialization
connection: duckdb-default

# TODO: Choose materialization (optional, but recommended).
# Bruin feature: Python materialization lets you return a DataFrame (or list[dict]) and Bruin loads it into your destination.
# This is usually the easiest way to build ingestion assets in Bruin.
# Alternative (advanced): you can skip Bruin Python materialization and write a "plain" Python asset that manually writes
# into DuckDB (or another destination) using your own client library and SQL. In that case:
# - you typically omit the `materialization:` block
# - you do NOT need a `materialize()` function; you just run Python code
# Docs: https://getbruin.com/docs/bruin/assets/python#materialization
materialization:
  # TODO: choose `table` or `view` (ingestion generally should be a table)
  type: table
  # TODO: pick a strategy.
  # suggested strategy: append
  strategy: append

# TODO: Define output columns (names + types) for metadata, lineage, and quality checks.
# Tip: mark stable identifiers as `primary_key: true` if you plan to use `merge` later.
# Docs: https://getbruin.com/docs/bruin/assets/columns
columns:
  - name: trip_id
    type: integer
    description: Unique trip identifier
  - name: taxi_type
    type: string
    description: Type of taxi (yellow, green, etc)
  - name: pickup_datetime
    type: string
    description: Pickup date and time
  - name: dropoff_datetime
    type: string
    description: Dropoff date and time
  - name: passenger_count
    type: integer
    description: Number of passengers
  - name: trip_distance
    type: float
    description: Trip distance in miles
  - name: fare_amount
    type: float
    description: Fare amount in dollars
  - name: extracted_at
    type: timestamp
    description: Timestamp when data was extracted

@bruin"""

import os
import json
import pandas as pd
from datetime import datetime


def materialize():
    """
    Ingests NYC Taxi trip data using Bruin runtime context.

    Required Bruin concepts to use here:
    - Built-in date window variables:
      - BRUIN_START_DATE / BRUIN_END_DATE (YYYY-MM-DD)
      - BRUIN_START_DATETIME / BRUIN_END_DATETIME (ISO datetime)
      Docs: https://getbruin.com/docs/bruin/assets/python#environment-variables
    - Pipeline variables:
      - Read JSON from BRUIN_VARS, e.g. `taxi_types`
      Docs: https://getbruin.com/docs/bruin/getting-started/pipeline-variables

    Design TODOs (keep logic minimal, focus on architecture):
    - Use start/end dates + `taxi_types` to generate a list of source endpoints for the run window.
    - Fetch data for each endpoint, parse into DataFrames, and concatenate.
    - Add a column like `extracted_at` for lineage/debugging (timestamp of extraction).
    - Prefer append-only in ingestion; handle duplicates in staging.
    """
    # Get Bruin environment variables
    start_date = os.getenv("BRUIN_START_DATE")
    end_date = os.getenv("BRUIN_END_DATE")
    
    # Get pipeline variables
    bruin_vars = os.getenv("BRUIN_VARS", "{}")
    variables = json.loads(bruin_vars)
    taxi_types = variables.get("taxi_types", ["yellow"])
    
    # TODO: Implement actual data fetching logic here
    # For now, return a minimal DataFrame to allow the pipeline to run
    data = {
        "trip_id": [1, 2, 3],
        "taxi_type": [taxi_types[0]] * 3,
        "pickup_datetime": [start_date] * 3,
        "dropoff_datetime": [end_date] * 3,
        "passenger_count": [1, 2, 1],
        "trip_distance": [2.5, 5.1, 1.2],
        "fare_amount": [10.0, 18.5, 7.5],
        "extracted_at": [datetime.now()] * 3
    }
    
    return pd.DataFrame(data)


