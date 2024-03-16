CREATE DATABASE IF NOT EXISTS ts_dev_db;
CREATE USER IF NOT EXISTS 'ts_dev'@'localhost' IDENTIFIED BY 'ts_dev_pwd';
GRANT ALL PRIVILEGES ON `ts_dev_db`.* TO 'ts_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'ts_dev'@'localhost';
FLUSH PRIVILEGES;