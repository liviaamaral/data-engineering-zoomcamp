"""
Question 2: Producer - send Green Taxi trip data to Redpanda topic 'green-trips'.
"""

import json
from time import time

import pandas as pd
from kafka import KafkaProducer

TOPIC = "green-trips"
BOOTSTRAP_SERVERS = "localhost:9092"
PARQUET_FILE = "../green_tripdata_2025-10.parquet"

COLUMNS = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
    "PULocationID",
    "DOLocationID",
    "passenger_count",
    "trip_distance",
    "tip_amount",
    "total_amount",
]


def main():
    df = pd.read_parquet(PARQUET_FILE, columns=COLUMNS)

    # Convert datetime columns to strings for JSON serialization
    for col in ["lpep_pickup_datetime", "lpep_dropoff_datetime"]:
        df[col] = df[col].astype(str)

    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    t0 = time()

    for _, row in df.iterrows():
        producer.send(TOPIC, value=row.to_dict())

    producer.flush()

    t1 = time()
    print(f"Sent {len(df)} rows in {(t1 - t0):.2f} seconds")


if __name__ == "__main__":
    main()
