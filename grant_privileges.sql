-- Grant all privileges to the specified user on a specific database
GRANT ALL PRIVILEGES ON %MYSQL_DATABASE%.* TO '%MYSQL_USER%'@'%' IDENTIFIED BY '%MYSQL_PASSWORD%';

-- Flush privileges to apply the changes
FLUSH PRIVILEGES;
