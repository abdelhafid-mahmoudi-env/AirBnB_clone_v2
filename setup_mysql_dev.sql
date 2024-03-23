-- Ensures that the database hbnb_dev_db is created if it doesn't already exist.
-- This statement creates the database that will be used for development purposes.
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Creates a MySQL user 'hbnb_dev' identified by the specified password if the user doesn't already exist.
-- This user will be associated with the localhost, restricting access to the local machine.
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grants all privileges on the hbnb_dev_db database to the user 'hbnb_dev'.
-- This statement provides full access to the specified database for the 'hbnb_dev' user.
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Grants SELECT privilege on the performance_schema database to 'hbnb_dev'.
-- The performance_schema database is used for performance monitoring, and granting SELECT privileges allows the 'hbnb_dev' user to access performance-related information.
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Flushes the privileges to apply the changes immediately.
-- This statement ensures that any recent privilege modifications take effect without requiring a server restart.
FLUSH PRIVILEGES;
