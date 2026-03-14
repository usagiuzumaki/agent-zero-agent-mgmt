#!/bin/bash
SESSION_SECRET=test python3 run_ui.py > server_test.log 2>&1 &
SERVER_PID=$!
sleep 15
if kill -0 $SERVER_PID 2>/dev/null; then
    kill $SERVER_PID
    cat server_test.log
    exit 0
else
    cat server_test.log
    exit 1
fi
