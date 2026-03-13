-- Run before starting the Flink jobs (Q4, Q5, Q6)
-- psql -h localhost -U postgres -d postgres -f create_tables.sql

-- Q4: Tumbling 5-minute window per PULocationID
CREATE TABLE IF NOT EXISTS green_trips_tumbling_5min (
    window_start  TIMESTAMP,
    "PULocationID" INT,
    num_trips     BIGINT,
    PRIMARY KEY (window_start, "PULocationID")
);

-- Q5: Session window (5-min gap) per PULocationID
CREATE TABLE IF NOT EXISTS green_trips_session (
    window_start  TIMESTAMP,
    window_end    TIMESTAMP,
    "PULocationID" INT,
    num_trips     BIGINT,
    PRIMARY KEY (window_start, window_end, "PULocationID")
);

-- Q6: Tumbling 1-hour window — total tip per hour
CREATE TABLE IF NOT EXISTS green_trips_tip_per_hour (
    window_start TIMESTAMP PRIMARY KEY,
    total_tip    DOUBLE PRECISION
);
