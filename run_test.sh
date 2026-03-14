SESSION_SECRET=test python3 run_ui.py > server_test.log 2>&1 &
SERVER_PID=$!
sleep 15
kill $SERVER_PID
cat server_test.log
