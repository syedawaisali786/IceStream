# IceStream — Week 2: Lakehouse Foundation

## Completed Components

- Apache Kafka topic: `icestream-transactions`
- Apache Flink 2.3.0 local cluster
- Apache Iceberg catalog using Hadoop catalog
- Iceberg warehouse: `C:/flink/iceberg-warehouse`
- Iceberg database: `icestream`
- Iceberg table: `transactions`
- Kafka → Flink streaming source
- Flink → Iceberg streaming pipeline
- NULL-rate data-quality validation for `tax_amount`
- Iceberg snapshot history verification

## Data Quality Rule

The pipeline checks the percentage of NULL values in `tax_amount`.

Threshold:

- NULL percentage <= 10% → PASS
- NULL percentage > 10% → FAIL

## Pipeline

Kafka
→ Apache Flink
→ Apache Iceberg

## Iceberg Table

`icestream.transactions`

Columns:

- transaction_id
- timestamp
- product
- amount
- tax_amount
- region
- payment_status
- customer_type

## Status

Week 2 lakehouse foundation and streaming pipeline implemented.
