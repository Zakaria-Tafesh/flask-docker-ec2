#!/bin/bash

set -e

# Replace environment variables in the SQL template and create the SQL file
sed -e "s/\${MYSQL_DATABASE}/$MYSQL_DATABASE/g" \
    -e "s/\${MYSQL_USER}/$MYSQL_USER/g" \
    -e "s/\${MYSQL_PASSWORD}/$MYSQL_PASSWORD/g" /docker-entrypoint-initdb.d/init_template.sql > /docker-entrypoint-initdb.d/init.sql

# Start MySQL with the generated SQL file
/docker-entrypoint.sh mysqld
