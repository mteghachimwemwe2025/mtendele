#!/bin/bash

echo "🔁 Starting Flask server with gunicorn..."

until gunicorn run:app -b 0.0.0.0:5000; do
  echo "❌ Server crashed with exit code $?. Restarting in 3 seconds..." >&2
  sleep 3
done
