"""
IceStream - Week 2 Data Quality Rules

Validates the NULL rate of tax_amount in transaction records.
"""

NULL_RATE_THRESHOLD = 0.10


def check_tax_amount_quality(records):
    """
    Check whether the tax_amount NULL rate is within the allowed threshold.

    Returns:
        dict: quality metrics and PASS/FAIL status.
    """
    total_records = len(records)

    if total_records == 0:
        return {
            "total_records": 0,
            "null_tax_records": 0,
            "null_percentage": 0.0,
            "status": "PASS",
        }

    null_tax_records = sum(
        1 for record in records
        if record.get("tax_amount") is None
    )

    null_percentage = (null_tax_records / total_records) * 100

    status = (
        "FAIL"
        if null_percentage > NULL_RATE_THRESHOLD * 100
        else "PASS"
    )

    return {
        "total_records": total_records,
        "null_tax_records": null_tax_records,
        "null_percentage": round(null_percentage, 2),
        "status": status,
    }


if __name__ == "__main__":
    sample_records = [
        {"transaction_id": "1", "tax_amount": 180.0},
        {"transaction_id": "2", "tax_amount": 250.0},
        {"transaction_id": "3", "tax_amount": None},
        {"transaction_id": "4", "tax_amount": 100.0},
    ]

    result = check_tax_amount_quality(sample_records)

    print("IceStream Data Quality Check")
    print("============================")
    print("Total records:", result["total_records"])
    print("NULL tax records:", result["null_tax_records"])
    print("NULL percentage:", result["null_percentage"], "%")
    print("Status:", result["status"])
