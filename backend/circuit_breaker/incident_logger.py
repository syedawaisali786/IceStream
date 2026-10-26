import json
from datetime import datetime, timezone
from pathlib import Path

INCIDENT_LOG = (
    Path(__file__).resolve().parent / "incident_log.jsonl"
)


def log_incident(
    incident_type,
    severity,
    description,
    transaction_ids=None,
    action="",
    recovery_status="PENDING",
):
    """Append one incident record to the local JSONL log."""

    incident = {
        "incident_id": datetime.now(timezone.utc).strftime(
            "%Y%m%dT%H%M%S%fZ"
        ),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "incident_type": incident_type,
        "severity": severity,
        "description": description,
        "transaction_ids": transaction_ids or [],
        "action": action,
        "recovery_status": recovery_status,
    }

    INCIDENT_LOG.parent.mkdir(parents=True, exist_ok=True)

    with INCIDENT_LOG.open("a", encoding="utf-8") as file:
        file.write(json.dumps(incident) + "\n")

    return incident


if __name__ == "__main__":
    record = log_incident(
        incident_type="DATA_QUALITY_FAILURE",
        severity="HIGH",
        description="Null tax_amount values exceeded the quality threshold.",
        transaction_ids=["TX-003", "TX-004", "TX-007"],
        action="Circuit breaker opened; records routed to Kafka DLQ.",
        recovery_status="QUARANTINED",
    )

    print(json.dumps(record, indent=2))
    print(f"\nIncident log: {INCIDENT_LOG}")