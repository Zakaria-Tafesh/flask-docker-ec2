#!/bin/bash

MYSQL_USER=${MYSQL_USER}
MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
MYSQL_DATABASE=${MYSQL_DATABASE}
MYSQL_PASSWORD=${MYSQL_PASSWORD}


QUERY="SELECT CONCAT('The user is: ', '$MYSQL_USER');"

mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "$QUERY"

