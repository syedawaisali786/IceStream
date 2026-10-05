from circuit_breaker import CircuitBreaker
from dlq_handler import DeadLetterQueue


def process_records(records):
    total_records = len(records)

    failed_records = sum(
        1 for record in records
        if record.get("tax_amount") is None
    )

    breaker = CircuitBreaker()
    dlq = DeadLetterQueue()

    result = breaker.evaluate(
        total_records,
        failed_records
    )

    print("IceStream Pipeline Guard")
    print("========================")
    print("Total records:", total_records)
    print("Failed records:", failed_records)
    print("Error rate:", result["error_rate"], "%")
    print("Circuit state:", result["state"])
    print("Action:", result["action"])

    if result["state"] == "OPEN":
        print("\n⚠ CIRCUIT BREAKER OPEN")
        print("Routing invalid records to DLQ...\n")

        for record in records:
            if record.get("tax_amount") is None:
                dlq.quarantine(
                    record,
                    "Tax amount is NULL"
                )

        print("DLQ records:", dlq.count())

    else:
        print("\n✓ Pipeline continues normally")

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