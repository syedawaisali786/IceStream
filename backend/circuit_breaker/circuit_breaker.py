ERROR_RATE_THRESHOLD = 0.02  # 2%


class CircuitBreaker:
    def __init__(self):
        self.state = "CLOSED"

    def evaluate(self, total_records, failed_records):
        if total_records == 0:
            return {
                "state": self.state,
                "error_rate": 0.0,
                "action": "NO_DATA"
            }

        error_rate = failed_records / total_records

        if error_rate > ERROR_RATE_THRESHOLD:
            self.state = "OPEN"
            action = "ROUTE_TO_DLQ"
        else:
            self.state = "CLOSED"
            action = "CONTINUE_PIPELINE"

        return {
            "state": self.state,
            "error_rate": round(error_rate * 100, 2),
            "action": action
        }


if __name__ == "__main__":
    breaker = CircuitBreaker()

    result = breaker.evaluate(
        total_records=100,
        failed_records=5
    )

    print("IceStream Circuit Breaker")
    print("=========================")
    print("Error Rate:", result["error_rate"], "%")
    print("State:", result["state"])
    print("Action:", result["action"])