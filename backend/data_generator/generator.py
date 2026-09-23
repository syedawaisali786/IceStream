import random
import time
import uuid
import json
from datetime import datetime, timezone

from kafka import KafkaProducer


KAFKA_SERVER = "localhost:9092"
KAFKA_TOPIC = "icestream-transactions"


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


producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)


def generate_transaction():

    amount = round(random.uniform(100, 50000), 2)
    tax_amount = round(amount * 0.18, 2)

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

    # Simulate schema drift occasionally
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
    print("Kafka server:", KAFKA_SERVER)
    print("Kafka topic:", KAFKA_TOPIC)
    print("Generating transactions...")
    print("Press CTRL + C to stop.\n")

    try:

        while True:

            transaction = generate_transaction()

            producer.send(
                KAFKA_TOPIC,
                value=transaction
            )

            producer.flush()

            print(
                "Sent to Kafka:",
                transaction["transaction_id"]
            )

            time.sleep(1)

    except KeyboardInterrupt:

        print("\nStopping transaction generator...")

    finally:

        producer.close()


if __name__ == "__main__":
    main()