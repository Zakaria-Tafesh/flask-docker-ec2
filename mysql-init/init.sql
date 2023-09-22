-- Debug: Print environment variables
SELECT 'Debugging message 1';

SELECT '${MYSQL_USER}', '${MYSQL_PASSWORD}', '${MYSQL_DATABASE}';

CREATE DATABASE IF NOT EXISTS '${MYSQL_DATABASE}';

-- Use the created database
USE '${MYSQL_DATABASE}';

-- Create the user and grant privileges
CREATE USER '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'%';

