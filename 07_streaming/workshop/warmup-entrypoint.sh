#!/bin/bash

# Workaround for Flink 2.2.0 bug: StaticFileServerHandler.respondToRequest uses
# Files.copy(stream, path) without REPLACE_EXISTING. When the browser makes
# parallel requests on first load, concurrent threads all see !file.exists()=true,
# all attempt the copy, and all but one fail with FileAlreadyExistsException,
# which is caught but sets success=false → NotFoundException → browser error.
#
# Fix: make one sequential warmup request before external traffic reaches the
# server, so index.html is already extracted and all future requests skip the
# copy step entirely (file.exists() = true).

_sigterm_handler() {
    if [ -n "$FLINK_PID" ]; then
        kill -TERM "$FLINK_PID" 2>/dev/null
    fi
}
trap _sigterm_handler SIGTERM SIGINT

# Start Flink using the original entrypoint (in background so we can warm up)
/docker-entrypoint.sh "$@" &
FLINK_PID=$!

if [ "$1" = "jobmanager" ]; then
    echo "⏳ Waiting for Flink REST server on port 8081 (up to 60s)..."
    READY=false
    for i in $(seq 1 60); do
        if curl -sf http://localhost:8081/config > /dev/null 2>&1; then
            READY=true
            break
        fi
        sleep 1
    done

    if [ "$READY" = "true" ]; then
        echo "Pre-warming Flink Web UI (workaround for race condition bug)..."
        curl -sf http://localhost:8081/ > /dev/null 2>&1 || true
        echo "Flink Web UI ready at http://localhost:8081"
    else
        echo "REST server did not start within 60s, skipping pre-warm."
    fi
fi

wait $FLINK_PID
exit $?
