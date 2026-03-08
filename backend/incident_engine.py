from datetime import datetime
from backend.models import Incident, ServiceMetric


def detect_incident(service_metric: ServiceMetric):
    if service_metric.uptime_percent < 95:
        return Incident(
            timestamp=datetime.now(),
            service=service_metric.name,
            severity="Critical",
            issue="Service outage detected",
            possible_cause="Service unavailable or infrastructure failure",
            recommended_action="Check service availability, restart affected service, and investigate infrastructure logs"
        )

    if service_metric.response_time_ms > 400:
        return Incident(
            timestamp=datetime.now(),
            service=service_metric.name,
            severity="Critical",
            issue="High latency detected",
            possible_cause="Database overload, network congestion, or traffic spike",
            recommended_action="Review backend logs, inspect database performance, and check network health"
        )

    if service_metric.error_rate_percent > 5:
        return Incident(
            timestamp=datetime.now(),
            service=service_metric.name,
            severity="Critical",
            issue="High error rate detected",
            possible_cause="Application exceptions, failed integrations, or backend processing issues",
            recommended_action="Inspect error logs, identify failing endpoints, and validate dependent services"
        )

    if 250 < service_metric.response_time_ms <= 400:
        return Incident(
            timestamp=datetime.now(),
            service=service_metric.name,
            severity="Warning",
            issue="Performance degradation detected",
            possible_cause="Increased processing time or moderate system load",
            recommended_action="Monitor service closely and review recent traffic or query patterns"
        )

    if 2 < service_metric.error_rate_percent <= 5:
        return Incident(
            timestamp=datetime.now(),
            service=service_metric.name,
            severity="Warning",
            issue="Elevated error rate detected",
            possible_cause="Minor service instability or intermittent request failures",
            recommended_action="Review logs and monitor for escalation"
        )

    return None


def detect_all_incidents(service_metrics):
    incidents = []

    for metric in service_metrics:
        incident = detect_incident(metric)
        if incident:
            incidents.append(incident)

    return incidents