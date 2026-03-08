from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ServiceMetric(BaseModel):
    name: str
    status: str
    response_time_ms: float
    error_rate_percent: float
    uptime_percent: float
    last_checked: datetime


class Incident(BaseModel):
    timestamp: datetime
    service: str
    severity: str
    issue: str
    possible_cause: str
    recommended_action: Optional[str] = None