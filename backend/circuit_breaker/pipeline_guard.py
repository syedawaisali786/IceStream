import json
from datetime import datetime, timezone
from kafka import KafkaProducer

from circuit_breaker import CircuitBreaker

KAFKA_SERVER = "localhost:9092"
DLQ_TOPIC = "icestream-dlq"


def process_records(records):
    total_records = len(records)

    failed_records = sum(
        1 for record in records
        if record.get("tax_amount") is None
    )

    breaker = CircuitBreaker()
    result = breaker.evaluate(total_records, failed_records)

    print("IceStream Pipeline Guard")
    print("========================")
    print("Total records:", total_records)
    print("Failed records:", failed_records)
    print("Error rate:", result["error_rate"], "%")
    print("Circuit state:", result["state"])
    print("Action:", result["action"])

    if result["state"] == "OPEN":
        print("Circuit breaker OPEN. Sending invalid records to Kafka DLQ.")

        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda value: json.dumps(value).encode("utf-8")
        )

        try:
            for record in records:
                if record.get("tax_amount") is None:
                    dlq_record = {
                        **record,
                        "quarantined_at": datetime.now(
                            timezone.utc
                        ).isoformat(),
                        "failure_reason": "Tax amount is NULL"
                    }

                    producer.send(DLQ_TOPIC, value=dlq_record)
                    print("Quarantined:", record.get("transaction_id"))

            producer.flush()
            print("DLQ messages sent successfully.")

        finally:
            producer.close()

    else:
        print("Pipeline continues normally.")

    return result


if __name__ == "__main__":
    sample_records = [
        {"transaction_id": "TX-001", "tax_amount": 180.0},
        {"transaction_id": "TX-002", "tax_amount": 250.0},
        {"transaction_id": "TX-003", "tax_amount": None},
        {"transaction_id": "TX-004", "tax_amount": None},
        {"transaction_id": "TX-005", "tax_amount": 100.0},
        {"transaction_id": "TX-006", "tax_amount": 200.0},
        {"transaction_id": "TX-007", "tax_amount": None},
        {"transaction_id": "TX-008", "tax_amount": 150.0},
        {"transaction_id": "TX-009", "tax_amount": 300.0},
        {"transaction_id": "TX-010", "tax_amount": 120.0},
    ]

    process_records(sample_records)