#!/bin/bash

# Function to check if MySQL is up and running
mysql_is_up() {
  mysqladmin ping -h localhost --silent
}

# Wait for MySQL to become available
while ! mysql_is_up; do
  echo "Waiting for MySQL to become available..."
  sleep 10
done

# Once MySQL is up, run your query script
/usr/local/bin/query.sh
