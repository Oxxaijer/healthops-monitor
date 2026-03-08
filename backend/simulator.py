import random
from datetime import datetime
from backend.models import ServiceMetric


SERVICE_NAMES = [
    "Patient Records API",
    "Appointment Booking API",
    "Lab Results API",
    "Pharmacy Service API",
    "Authentication Service"
]


def determine_status(response_time_ms: float, error_rate_percent: float, uptime_percent: float) -> str:
    if uptime_percent < 95:
        return "Down"
    elif response_time_ms > 400 or error_rate_percent > 5:
        return "Critical"
    elif response_time_ms > 250 or error_rate_percent > 2:
        return "Warning"
    return "Healthy"


def generate_service_metric(service_name: str) -> ServiceMetric:
    response_time_ms = round(random.uniform(80, 550), 2)
    error_rate_percent = round(random.uniform(0.1, 8.0), 2)
    uptime_percent = round(random.uniform(93.0, 100.0), 2)

    status = determine_status(response_time_ms, error_rate_percent, uptime_percent)

    return ServiceMetric(
        name=service_name,
        status=status,
        response_time_ms=response_time_ms,
        error_rate_percent=error_rate_percent,
        uptime_percent=uptime_percent,
        last_checked=datetime.now()
    )


def generate_all_service_metrics():
    return [generate_service_metric(service_name) for service_name in SERVICE_NAMES]