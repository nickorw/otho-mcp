#!/bin/bash
set -e

# Start Tomcat (OOPs) in background
$CATALINA_HOME/bin/catalina.sh start

# Wait for OOPs to be ready
for i in $(seq 1 30); do
    if curl -sf http://localhost:8080/OOPS/rest > /dev/null 2>&1; then
        break
    fi
    sleep 1
done

# Start MCP server (foreground)
exec python -m src.server
