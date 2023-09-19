#!/bin/bash

# Load environment variables from .env file
set -o allexport
#source .env
set +o allexport

# Replace placeholders in the template SQL file and save it as grant_privileges.sql
sed -e "s|%MYSQL_DATABASE%|${MYSQL_DATABASE}|g" \
    -e "s|%MYSQL_USER%|${MYSQL_USER}|g" \
    -e "s|%MYSQL_PASSWORD%|${MYSQL_PASSWORD}|g" \
    grant_privileges_template.sql > grant_privileges.sql

# Clean up
rm grant_privileges_template.sql
