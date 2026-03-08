from pathlib import Path
from datetime import datetime
import csv

from backend.simulator import generate_all_service_metrics
from backend.incident_engine import detect_all_incidents

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

SERVICE_METRICS_FILE = DATA_DIR / "service_metrics.csv"
INCIDENTS_FILE = DATA_DIR / "incidents.csv"


def ensure_directories_and_files():
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)

    if not SERVICE_METRICS_FILE.exists():
        with open(SERVICE_METRICS_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp",
                "service",
                "status",
                "response_time_ms",
                "error_rate_percent",
                "uptime_percent"
            ])

    if not INCIDENTS_FILE.exists():
        with open(INCIDENTS_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp",
                "service",
                "severity",
                "issue",
                "possible_cause",
                "recommended_action"
            ])


def save_service_metrics(services):
    ensure_directories_and_files()

    with open(SERVICE_METRICS_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for service in services:
            writer.writerow([
                service.last_checked.strftime("%Y-%m-%d %H:%M:%S"),
                service.name,
                service.status,
                service.response_time_ms,
                service.error_rate_percent,
                service.uptime_percent
            ])


def save_incidents(incidents):
    ensure_directories_and_files()

    with open(INCIDENTS_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for incident in incidents:
            writer.writerow([
                incident.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                incident.service,
                incident.severity,
                incident.issue,
                incident.possible_cause,
                incident.recommended_action
            ])


def generate_incident_report(incident):
    ensure_directories_and_files()

    timestamp_str = incident.timestamp.strftime("%Y-%m-%d_%H-%M-%S")
    safe_service_name = incident.service.replace(" ", "_").replace("/", "_")
    report_file = REPORTS_DIR / f"incident_{safe_service_name}_{timestamp_str}.txt"

    report_content = f"""HealthOps Monitor Incident Report

Timestamp: {incident.timestamp.strftime("%Y-%m-%d %H:%M:%S")}
Service: {incident.service}
Severity: {incident.severity}

Issue:
{incident.issue}

Possible Cause:
{incident.possible_cause}

Recommended Action:
{incident.recommended_action}
"""

    with open(report_file, "w", encoding="utf-8") as file:
        file.write(report_content)


def generate_reports_for_critical_incidents(incidents):
    for incident in incidents:
        if incident.severity == "Critical":
            generate_incident_report(incident)


def get_services():
    services = generate_all_service_metrics()
    save_service_metrics(services)
    return services


def get_incidents():
    services = generate_all_service_metrics()
    incidents = detect_all_incidents(services)
    save_incidents(incidents)
    generate_reports_for_critical_incidents(incidents)
    return incidents


def get_summary():
    services = generate_all_service_metrics()
    incidents = detect_all_incidents(services)

    save_service_metrics(services)
    save_incidents(incidents)
    generate_reports_for_critical_incidents(incidents)

    total_services = len(services)

    healthy_services = sum(1 for s in services if s.status == "Healthy")
    warning_services = sum(1 for s in services if s.status == "Warning")
    critical_services = sum(1 for s in services if s.status == "Critical")
    down_services = sum(1 for s in services if s.status == "Down")

    avg_response = round(
        sum(s.response_time_ms for s in services) / total_services, 2
    ) if total_services > 0 else 0

    avg_error = round(
        sum(s.error_rate_percent for s in services) / total_services, 2
    ) if total_services > 0 else 0

    avg_uptime = round(
        sum(s.uptime_percent for s in services) / total_services, 2
    ) if total_services > 0 else 0

    return {
        "total_services": total_services,
        "healthy_services": healthy_services,
        "warning_services": warning_services,
        "critical_services": critical_services,
        "down_services": down_services,
        "active_incidents": len(incidents),
        "average_response_time_ms": avg_response,
        "average_error_rate_percent": avg_error,
        "average_uptime_percent": avg_uptime
    }