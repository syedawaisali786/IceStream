USE CATALOG iceberg_catalog;
USE icestream;

-- Check transaction count
SELECT COUNT(*) AS total_transactions
FROM transactions;

-- View Iceberg snapshot history
SELECT committed_at, snapshot_id, operation
FROM transactions$snapshots;

-- View sample transactions
SELECT *
FROM transactions
LIMIT 10;