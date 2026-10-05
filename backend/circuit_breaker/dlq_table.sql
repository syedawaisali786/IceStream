CREATE TABLE dlq_transactions (
    transaction_id STRING,
    `timestamp` STRING,
    product STRING,
    amount DOUBLE,
    tax_amount DOUBLE,
    region STRING,
    payment_status STRING,
    customer_type STRING,
    quarantined_at STRING,
    failure_reason STRING
) WITH (
    'format-version' = '2'
);