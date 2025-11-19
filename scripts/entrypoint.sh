#!/usr/bin/env bash
set -e

# Wait for services to be up before starting the given command.
python /app/scripts/wait_for_services.py

# Run the command passed to container
exec "$@"
