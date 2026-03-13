"""
Question 4: Tumbling 5-minute window — count trips per PULocationID.

Submit from host:
  docker exec -it workshop-jobmanager-1 flink run \
      -py /opt/homework/q4_tumbling_pickup.py -d

Result table: green_trips_tumbling_5min
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
    'properties.group.id' = 'flink-q4',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'json'
)
""")

# Sink
t_env.execute_sql(f"""
CREATE TABLE green_trips_tumbling_5min (
    window_start  TIMESTAMP(3),
    pulocationid  INT,
    num_trips     BIGINT,
    PRIMARY KEY (window_start, pulocationid) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = '{PG_URL}',
    'table-name' = 'green_trips_tumbling_5min',
    'username' = '{PG_USER}',
    'password' = '{PG_PASS}'
)
""")

# Job
t_env.execute_sql("""
INSERT INTO green_trips_tumbling_5min
SELECT
    TUMBLE_START(event_timestamp, INTERVAL '5' MINUTE) AS window_start,
    PULocationID AS pulocationid,
    COUNT(*) AS num_trips
FROM green_trips
GROUP BY
    TUMBLE(event_timestamp, INTERVAL '5' MINUTE),
    PULocationID
""")
