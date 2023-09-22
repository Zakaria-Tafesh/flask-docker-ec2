#!/bin/bash

echo "Starting query.sh ..."

mysql_is_up() {
  mysqladmin ping -h localhost --silent
}

# Wait for MySQL to become available
#while ! mysql_is_up; do
#  echo "Waiting for MySQL to become available..."
#  sleep 5
#done
#
#echo "MySQL is available now ..."
#
#MYSQL_USER=${MYSQL_USER}
#MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
#MYSQL_DATABASE=${MYSQL_DATABASE}
#MYSQL_PASSWORD=${MYSQL_PASSWORD}
#
#
#QUERY="SELECT CONCAT('The user is: ', '$MYSQL_USER');"
#
#mysql -u root -p"$MYSQL_ROOT_PASSWORD" -S /var/run/mysqld/mysqld.sock -e "$QUERY"

