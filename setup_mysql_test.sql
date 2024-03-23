-- Ensures the creation of the test database hbnb_test_db if it doesn't already exist.
-- This statement creates the database intended for testing purposes.
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Creates a MySQL user 'hbnb_test' identified by the specified password if the user doesn't already exist.
-- This user is specifically designated for testing, associated only with the localhost.
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grants all privileges on the hbnb_test_db database to the user 'hbnb_test'.
-- The user 'hbnb_test' is given full access to the test database for executing test cases.
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grants SELECT privilege on the performance_schema database to 'hbnb_test'.
-- Granting SELECT privileges on the performance_schema database allows 'hbnb_test' to access performance-related data during testing.
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Flushes privileges to apply the changes immediately.
-- This statement ensures that any recent privilege modifications take effect without needing a server restart.
FLUSH PRIVILEGES;
