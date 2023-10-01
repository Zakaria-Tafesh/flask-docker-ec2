-- Debug: Print environment variables
SELECT 'Debugging message 1';

SELECT '${MYSQL_USER}', '${MYSQL_PASSWORD}', '${MYSQL_DATABASE}';

-- Create a sample table
CREATE TABLE IF NOT EXISTS my_table2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name2 VARCHAR(255) NOT NULL
);
