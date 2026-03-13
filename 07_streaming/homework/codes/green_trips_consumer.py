"""
Question 3: Consumer - count trips with trip_distance > 5.0 km.
"""

import json

from kafka import KafkaConsumer

TOPIC = "green-trips"
BOOTSTRAP_SERVERS = "localhost:9092"


def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        consumer_timeout_ms=10_000,  # stop after 10s of inactivity
    )

    total = 0
    count_gt5 = 0

    for msg in consumer:
        trip = msg.value
        total += 1
        if trip.get("trip_distance", 0) > 5.0:
            count_gt5 += 1

    consumer.close()

    print(f"Total trips read : {total}")
    print(f"Trips with trip_distance > 5 km: {count_gt5}")


if __name__ == "__main__":
    main()
