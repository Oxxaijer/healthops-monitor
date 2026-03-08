# HealthOps Monitor
Healthcare Service Reliability Monitoring Platform

HealthOps Monitor is a system monitoring and incident intelligence platform designed to simulate how modern digital healthcare services can be observed, analysed, and supported operationally.

The platform continuously monitors simulated healthcare services, detects operational incidents, stores historical reliability data, and provides insights through an interactive monitoring dashboard.

This project demonstrates how operational monitoring systems can help ensure critical healthcare services remain reliable, responsive, and available for healthcare professionals and patients.

------------------------------------------------------------

PROJECT OVERVIEW

Modern healthcare systems depend heavily on digital infrastructure. Services such as patient records, appointment scheduling, authentication, laboratory results, and pharmacy systems must operate reliably at all times.

HealthOps Monitor simulates a real operational environment where multiple healthcare services are monitored continuously. The platform collects service metrics, detects anomalies, records incidents, and visualises system behaviour through a monitoring dashboard.

The goal of the project is to demonstrate how operational data can be used to understand system reliability and support digital healthcare infrastructure.

------------------------------------------------------------

KEY FEATURES

Service Monitoring

The platform monitors simulated healthcare services and tracks important operational metrics including:

- response time
- error rate
- service uptime
- service health status

Example services monitored include:

- Patient Records API
- Appointment Booking API
- Laboratory Results API
- Pharmacy Service API
- Authentication Service

------------------------------------------------------------

Incident Detection

The system includes an automated incident detection engine that evaluates service metrics and identifies abnormal system behaviour such as:

- performance degradation
- elevated error rates
- service outages
- instability in system responses

Detected incidents are categorised by severity and include contextual information describing the issue and potential causes.

------------------------------------------------------------

Operational Dashboard

An interactive monitoring dashboard provides real-time visibility into system health.

The dashboard displays:

- service health overview
- response time analysis
- error rate monitoring
- active incident logs
- incident severity distribution
- operational summary metrics

The interface allows system operators to quickly identify services experiencing issues.

------------------------------------------------------------

Historical Reliability Analytics

HealthOps Monitor stores operational data to support historical analysis of system behaviour.

The system generates insights such as:

- average response time per service
- service uptime trends
- incident frequency by service
- incident trends over time
- service stability ranking

These insights help identify long-term reliability patterns across services.

------------------------------------------------------------

Automated Incident Reports

When severe incidents are detected, the system automatically generates structured incident reports.

Each report includes:

- incident timestamp
- affected service
- severity level
- issue description
- possible cause
- recommended action

Reports are stored for operational review and documentation.

------------------------------------------------------------

SYSTEM ARCHITECTURE

Streamlit Monitoring Dashboard
        |
        | REST API
        |
FastAPI Backend
        |
        |-----------------------------
        |            |               |
Service Simulator    Incident Engine   Logging System
        |            |               |
        |------------|---------------|
                     |
             Historical Data Storage
                     |
             service_metrics.csv
             incidents.csv
                     |
               Incident Reports
                 reports/*.txt

------------------------------------------------------------

PROJECT STRUCTURE

healthops-monitor

backend
- main.py
- services.py
- simulator.py
- incident_engine.py
- models.py

dashboard
- app.py

data
- service_metrics.csv
- incidents.csv

reports
- incident report files generated automatically

requirements.txt
README.md
.gitignore

------------------------------------------------------------

TECHNOLOGY STACK

Backend API
FastAPI

Dashboard
Streamlit

Data Processing
Pandas

Data Visualisation
Plotly

Programming Language
Python

Data Storage
CSV log files for historical operational data

------------------------------------------------------------

RUNNING THE SYSTEM

Start the backend API

python3 -m uvicorn backend.main:app --reload --port 8001

Start the monitoring dashboard

streamlit run dashboard/app.py

Open the dashboard in your browser

http://localhost:8501

------------------------------------------------------------

EXAMPLE ANALYTICS

The platform provides operational insights including:

- services with the highest error rates
- services experiencing the most incidents
- average response time across systems
- uptime reliability trends
- incident distribution by severity

These insights help identify reliability issues and system performance patterns.

------------------------------------------------------------

FUTURE IMPROVEMENTS

Possible enhancements to the platform include:

- real-time alert notifications
- integration with monitoring systems
- predictive incident detection
- automated remediation workflows
- infrastructure monitoring integration
- persistent database storage

------------------------------------------------------------

## Dashboard Preview

### System Overview
![System Overview](screenshots/dashboard-system-overview.png)

### Live Service Metrics
![Live Metrics](screenshots/live-service-metrics.png)

### Incident Log
![Incident Log](screenshots/incident-management-log.png)

### Incident Severity Distribution
![Incident Severity](screenshots/incident-severity-distribution.png)

### Historical Reliability Analytics
![Reliability Analytics](screenshots/historical-reliability-analytics.png)

### Service Uptime Trend
![Uptime Trend](screenshots/service-uptime-trend.png)

### Incident Trend Analysis
![Incident Trend](screenshots/incident-trend-analysis.png)

### Service Stability Ranking
![Service Ranking](screenshots/service-stability-ranking.png)