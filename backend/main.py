from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.services import get_services, get_incidents, get_summary

app = FastAPI(
    title="HealthOps Monitor API",
    description="API for monitoring simulated healthcare digital services and incidents",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "HealthOps Monitor API is running",
        "endpoints": ["/services", "/incidents", "/summary"]
    }


@app.get("/services")
def services():
    services_list = get_services()
    return {
        "total_services": len(services_list),
        "services": [service.model_dump() for service in services_list]
    }


@app.get("/incidents")
def incidents():
    incidents_list = get_incidents()
    return {
        "total_incidents": len(incidents_list),
        "incidents": [incident.model_dump() for incident in incidents_list]
    }


@app.get("/summary")
def summary():
    return get_summary()