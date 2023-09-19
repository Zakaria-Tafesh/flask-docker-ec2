#!/bin/bash

# Start MySQL as a background process
mysqld &

# Wait for MySQL to start
until mysqladmin ping -h localhost --silent; do
    sleep 1
done

# Run your generate_sql.sh script
/generate_sql.sh

# Keep the container running by sleeping indefinitely
tail -f /dev/null
