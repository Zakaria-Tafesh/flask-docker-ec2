-- Debug: Print environment variables
SELECT '${MYSQL_USER}', '${MYSQL_PASSWORD}', '${MYSQL_DATABASE}';

-- Create the user and grant privileges
CREATE USER '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'%';

