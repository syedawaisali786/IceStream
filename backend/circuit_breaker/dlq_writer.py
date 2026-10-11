"""
IceStream - Iceberg Dead Letter Queue Writer

Writes quarantined transaction records to the Iceberg DLQ table.
"""

import json
import subprocess


FLINK_SQL_CLIENT = r"C:\flink\flink-2.3.0\bin\sql-client.sh"


def build_dlq_record(record, reason):
    """Prepare a transaction for DLQ storage."""

    return {
        "transaction_id": record.get("transaction_id"),
        "timestamp": record.get("timestamp"),
        "product": record.get("product"),
        "amount": record.get("amount"),
        "tax_amount": record.get("tax_amount"),
        "region": record.get("region"),
        "payment_status": record.get("payment_status"),
        "customer_type": record.get("customer_type"),
        "quarantined_at": record.get("quarantined_at"),
        "failure_reason": reason,
    }


def create_insert_statement(record, reason):
    """Create an Iceberg INSERT statement for a quarantined record."""

    dlq_record = build_dlq_record(record, reason)

    values = (
        f"'{dlq_record['transaction_id']}', "
        f"'{dlq_record['timestamp']}', "
        f"'{dlq_record['product']}', "
        f"{dlq_record['amount']}, "
        f"{'NULL' if dlq_record['tax_amount'] is None else dlq_record['tax_amount']}, "
        f"'{dlq_record['region']}', "
        f"'{dlq_record['payment_status']}', "
        f"'{dlq_record['customer_type']}', "
        f"'{dlq_record['quarantined_at']}', "
        f"'{dlq_record['failure_reason']}'"
    )

    return f"""
INSERT INTO icestream.dlq_transactions
VALUES ({values});
""".strip()


if __name__ == "__main__":

    sample_record = {
        "transaction_id": "TX-DLQ-001",
        "timestamp": "2026-10-05T10:00:00Z",
        "product": "Laptop",
        "amount": 50000.0,
        "tax_amount": None,
        "region": "Hyderabad",
        "payment_status": "SUCCESS",
        "customer_type": "NEW",
        "quarantined_at": "2026-10-05T10:01:00Z",
    }

    sql = create_insert_statement(
        sample_record,
        "Tax amount is NULL"
    )

    print("IceStream DLQ Writer")
    print("====================")
    print(sql)