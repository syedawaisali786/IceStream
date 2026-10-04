from datetime import datetime, timezone


class DeadLetterQueue:
    def __init__(self):
        self.records = []

    def quarantine(self, record, reason):
        dlq_record = {
            "quarantined_at": datetime.now(timezone.utc).isoformat(),
            "reason": reason,
            "record": record
        }

        self.records.append(dlq_record)

        return dlq_record

    def count(self):
        return len(self.records)


if __name__ == "__main__":
    dlq = DeadLetterQueue()

    bad_record = {
        "transaction_id": "TX-001",
        "tax_amount": None,
        "amount": 25000
    }

    result = dlq.quarantine(
        bad_record,
        "Tax amount is NULL"
    )

    print("IceStream Dead Letter Queue")
    print("===========================")
    print("Quarantined record:", result)
    print("DLQ records:", dlq.count())