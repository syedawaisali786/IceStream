import random
import time
import uuid
import json
from datetime import datetime, timezone


PRODUCTS = [
    "Laptop",
    "Smartphone",
    "Headphones",
    "Keyboard",
    "Mouse",
    "Monitor",
    "Smartwatch",
    "Tablet"
]

REGIONS = [
    "Hyderabad",
    "Bangalore",
    "Mumbai",
    "Delhi",
    "Chennai",
    "Pune"
]


def generate_transaction():

    # Generate transaction values
    amount = round(random.uniform(100, 50000), 2)
    tax_amount = round(amount * 0.18, 2)

    # Create transaction
    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "product": random.choice(PRODUCTS),
        "amount": amount,
        "tax_amount": tax_amount,
        "region": random.choice(REGIONS),
        "payment_status": random.choice([
            "SUCCESS",
            "SUCCESS",
            "SUCCESS",
            "FAILED"
        ])
    }

    # Inject NULL value occasionally
    if random.random() < 0.05:
        transaction["tax_amount"] = None

    # Simulate schema change occasionally
    if random.random() < 0.02:
        transaction["customer_type"] = random.choice([
            "NEW",
            "RETURNING",
            "VIP"
        ])

    return transaction


def main():

    print("========================================")
    print("       IceStream Transaction Generator")
    print("========================================")
    print("Generating e-commerce transactions...")
    print("Press CTRL + C to stop.\n")

    while True:

        transaction = generate_transaction()

        print(json.dumps(transaction))

        time.sleep(1)


if __name__ == "__main__":
    main()