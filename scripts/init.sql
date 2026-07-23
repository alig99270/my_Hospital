-- Hospital Management System Database Initialization Script
-- This script runs automatically when MySQL container starts for the first time

-- Grant privileges to the HMS user
GRANT ALL PRIVILEGES ON *.* TO 'hms_user'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

-- Set proper character set
ALTER DATABASE hms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
