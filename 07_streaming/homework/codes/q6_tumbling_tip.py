"""
Question 6: Tumbling 1-hour window — total tip_amount per hour (all locations).

Submit from host:
  docker exec -it workshop-jobmanager-1 flink run \
      -py /opt/homework/q6_tumbling_tip.py -d

Result table: green_trips_tip_per_hour
"""

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

KAFKA_BOOTSTRAP = "redpanda:29092"
KAFKA_TOPIC = "green-trips"
PG_URL = "jdbc:postgresql://postgres:5432/postgres"
PG_USER = "postgres"
PG_PASS = "postgres"

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)
t_env = StreamTableEnvironment.create(env)

# Source
t_env.execute_sql(f"""
CREATE TABLE green_trips (
    lpep_pickup_datetime  VARCHAR,
    lpep_dropoff_datetime VARCHAR,
    PULocationID          INT,
    DOLocationID          INT,
    passenger_count       DOUBLE,
    trip_distance         DOUBLE,
    tip_amount            DOUBLE,
    total_amount          DOUBLE,
    event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
    WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = '{KAFKA_TOPIC}',
    'properties.bootstrap.servers' = '{KAFKA_BOOTSTRAP}',
    'properties.group.id' = 'flink-q6',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'json'
)
""")

# Sink
t_env.execute_sql(f"""
CREATE TABLE green_trips_tip_per_hour (
    window_start TIMESTAMP(3),
    total_tip    DOUBLE,
    PRIMARY KEY (window_start) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = '{PG_URL}',
    'table-name' = 'green_trips_tip_per_hour',
    'username' = '{PG_USER}',
    'password' = '{PG_PASS}'
)
""")

# Job
t_env.execute_sql("""
INSERT INTO green_trips_tip_per_hour
SELECT
    TUMBLE_START(event_timestamp, INTERVAL '1' HOUR) AS window_start,
    SUM(tip_amount) AS total_tip
FROM green_trips
GROUP BY
    TUMBLE(event_timestamp, INTERVAL '1' HOUR)
""")
