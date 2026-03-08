import time
from pathlib import Path

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8001"
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SERVICE_METRICS_FILE = DATA_DIR / "service_metrics.csv"
INCIDENTS_FILE = DATA_DIR / "incidents.csv"

st.set_page_config(
    page_title="HealthOps Monitor",
    page_icon="🏥",
    layout="wide"
)


@st.cache_data(ttl=5)
def fetch_summary():
    response = requests.get(f"{API_BASE_URL}/summary", timeout=5)
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=5)
def fetch_services():
    response = requests.get(f"{API_BASE_URL}/services", timeout=5)
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=5)
def fetch_incidents():
    response = requests.get(f"{API_BASE_URL}/incidents", timeout=5)
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=5)
def load_historical_service_metrics():
    if SERVICE_METRICS_FILE.exists():
        df = pd.read_csv(SERVICE_METRICS_FILE)
        if not df.empty:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        return df
    return pd.DataFrame()


@st.cache_data(ttl=5)
def load_historical_incidents():
    if INCIDENTS_FILE.exists():
        df = pd.read_csv(INCIDENTS_FILE)
        if not df.empty:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        return df
    return pd.DataFrame()


def status_emoji(status: str) -> str:
    mapping = {
        "Healthy": "🟢",
        "Warning": "🟡",
        "Critical": "🔴",
        "Down": "⚫"
    }
    return mapping.get(status, "⚪")


def highlight_status(row):
    health = row["Health"]

    if health == "Healthy":
        return ["background-color: #d4edda"] * len(row)
    if health == "Warning":
        return ["background-color: #fff3cd"] * len(row)
    if health == "Critical":
        return ["background-color: #f8d7da"] * len(row)
    if health == "Down":
        return ["background-color: #e2e3e5"] * len(row)

    return [""] * len(row)


st.title("🏥 HealthOps Monitor")
st.caption("Digital Healthcare Service Operations Dashboard")

try:
    summary_data = fetch_summary()
    services_data = fetch_services()
    incidents_data = fetch_incidents()

    services_df = pd.DataFrame(services_data["services"])
    incidents_df = pd.DataFrame(incidents_data["incidents"])

    historical_services_df = load_historical_service_metrics()
    historical_incidents_df = load_historical_incidents()

    # Banner
    if summary_data["active_incidents"] > 0:
        st.error("🚨 SYSTEM INCIDENT DETECTED – Immediate attention required")
    else:
        st.success("✅ All Healthcare Services Operating Normally")

    # Current most unstable service
    if not services_df.empty:
        worst_service = services_df.sort_values("error_rate_percent", ascending=False).iloc[0]
        st.info(
            f"Most unstable live service: **{worst_service['name']}** "
            f"(Error rate: {worst_service['error_rate_percent']}%)"
        )

    # Summary cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Services", summary_data["total_services"])
    col2.metric("Healthy Services", summary_data["healthy_services"])
    col3.metric("Active Incidents", summary_data["active_incidents"])
    col4.metric("Avg Response Time", f'{summary_data["average_response_time_ms"]} ms')

    st.divider()

    # Service overview
    st.subheader("Service Health Overview")

    if not services_df.empty:
        services_df["status_indicator"] = services_df["status"].apply(status_emoji)
        services_df["last_checked"] = pd.to_datetime(
            services_df["last_checked"]
        ).dt.strftime("%Y-%m-%d %H:%M:%S")

        display_services_df = services_df[
            [
                "status_indicator",
                "name",
                "status",
                "response_time_ms",
                "error_rate_percent",
                "uptime_percent",
                "last_checked"
            ]
        ].rename(columns={
            "status_indicator": "Status",
            "name": "Service Name",
            "status": "Health",
            "response_time_ms": "Response Time (ms)",
            "error_rate_percent": "Error Rate (%)",
            "uptime_percent": "Uptime (%)",
            "last_checked": "Last Checked"
        })

        styled_services_df = display_services_df.style.apply(highlight_status, axis=1)
        st.dataframe(styled_services_df, use_container_width=True, hide_index=True)
    else:
        st.info("No service data available.")

    st.divider()

    # Live charts
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Live Response Time by Service")
        if not services_df.empty:
            fig_response = px.bar(
                services_df,
                x="name",
                y="response_time_ms",
                title="Current Service Response Time",
                labels={"name": "Service", "response_time_ms": "Response Time (ms)"}
            )
            st.plotly_chart(fig_response, use_container_width=True)
        else:
            st.info("No response time data available.")

    with chart_col2:
        st.subheader("Live Error Rate by Service")
        if not services_df.empty:
            fig_error = px.bar(
                services_df,
                x="name",
                y="error_rate_percent",
                title="Current Service Error Rate",
                labels={"name": "Service", "error_rate_percent": "Error Rate (%)"}
            )
            st.plotly_chart(fig_error, use_container_width=True)
        else:
            st.info("No error rate data available.")

    st.divider()

    # Live incidents
    st.subheader("Active Incident Log")

    if not incidents_df.empty:
        incidents_df["timestamp"] = pd.to_datetime(
            incidents_df["timestamp"]
        ).dt.strftime("%Y-%m-%d %H:%M:%S")

        display_incidents_df = incidents_df[
            [
                "timestamp",
                "service",
                "severity",
                "issue",
                "possible_cause",
                "recommended_action"
            ]
        ].rename(columns={
            "timestamp": "Timestamp",
            "service": "Service",
            "severity": "Severity",
            "issue": "Issue",
            "possible_cause": "Possible Cause",
            "recommended_action": "Recommended Action"
        })

        st.dataframe(display_incidents_df, use_container_width=True, hide_index=True)

        st.subheader("Incident Severity Distribution")
        severity_counts = incidents_df["severity"].value_counts().reset_index()
        severity_counts.columns = ["severity", "count"]

        fig_severity = px.pie(
            severity_counts,
            names="severity",
            values="count",
            title="Current Incident Severity Breakdown"
        )
        st.plotly_chart(fig_severity, use_container_width=True)
    else:
        st.success("No active incidents detected.")

    st.divider()

    # Historical analytics
    st.subheader("Historical Reliability Analytics")

    if not historical_services_df.empty:
        hist_col1, hist_col2 = st.columns(2)

        with hist_col1:
            avg_response_history = (
                historical_services_df
                .groupby("service", as_index=False)["response_time_ms"]
                .mean()
                .sort_values("response_time_ms", ascending=False)
            )

            fig_avg_response = px.bar(
                avg_response_history,
                x="service",
                y="response_time_ms",
                title="Average Historical Response Time by Service",
                labels={"service": "Service", "response_time_ms": "Avg Response Time (ms)"}
            )
            st.plotly_chart(fig_avg_response, use_container_width=True)

        with hist_col2:
            avg_uptime_history = (
                historical_services_df
                .groupby("service", as_index=False)["uptime_percent"]
                .mean()
                .sort_values("uptime_percent", ascending=True)
            )

            fig_avg_uptime = px.bar(
                avg_uptime_history,
                x="service",
                y="uptime_percent",
                title="Average Historical Uptime by Service",
                labels={"service": "Service", "uptime_percent": "Avg Uptime (%)"}
            )
            st.plotly_chart(fig_avg_uptime, use_container_width=True)

        st.subheader("Recent Uptime Trend")
        latest_metrics = (
            historical_services_df
            .sort_values("timestamp")
            .groupby("service", group_keys=False)
            .tail(10)
        )

        if not latest_metrics.empty:
            fig_uptime_trend = px.line(
                latest_metrics,
                x="timestamp",
                y="uptime_percent",
                color="service",
                title="Recent Uptime Trend by Service",
                labels={"timestamp": "Time", "uptime_percent": "Uptime (%)", "service": "Service"}
            )
            st.plotly_chart(fig_uptime_trend, use_container_width=True)

    else:
        st.info("No historical service metrics available yet.")

    if not historical_incidents_df.empty:
        hist_inc_col1, hist_inc_col2 = st.columns(2)

        with hist_inc_col1:
            incident_count_by_service = (
                historical_incidents_df["service"]
                .value_counts()
                .reset_index()
            )
            incident_count_by_service.columns = ["service", "count"]

            fig_incident_count = px.bar(
                incident_count_by_service,
                x="service",
                y="count",
                title="Historical Incident Count by Service",
                labels={"service": "Service", "count": "Incident Count"}
            )
            st.plotly_chart(fig_incident_count, use_container_width=True)

        with hist_inc_col2:
            historical_incidents_df["hour"] = historical_incidents_df["timestamp"].dt.floor("H")
            incident_trend = (
                historical_incidents_df
                .groupby("hour", as_index=False)
                .size()
            )
            incident_trend.columns = ["hour", "count"]

            fig_incident_trend = px.line(
                incident_trend,
                x="hour",
                y="count",
                title="Incident Trend Over Time",
                labels={"hour": "Time", "count": "Incident Count"}
            )
            st.plotly_chart(fig_incident_trend, use_container_width=True)

        ranking_df = (
            historical_incidents_df["service"]
            .value_counts()
            .reset_index()
        )
        ranking_df.columns = ["Service", "Historical Incident Count"]

        st.subheader("Service Stability Ranking")
        st.dataframe(ranking_df, use_container_width=True, hide_index=True)

    else:
        st.info("No historical incident data available yet.")

    st.divider()

    # Download section
    st.subheader("Downloads")

    dl_col1, dl_col2 = st.columns(2)

    with dl_col1:
        if SERVICE_METRICS_FILE.exists():
            with open(SERVICE_METRICS_FILE, "rb") as file:
                st.download_button(
                    label="Download Service Metrics CSV",
                    data=file,
                    file_name="service_metrics.csv",
                    mime="text/csv"
                )

    with dl_col2:
        if INCIDENTS_FILE.exists():
            with open(INCIDENTS_FILE, "rb") as file:
                st.download_button(
                    label="Download Incidents CSV",
                    data=file,
                    file_name="incidents.csv",
                    mime="text/csv"
                )

    st.divider()

    # Operational summary
    st.subheader("Operational Summary")
    insight_col1, insight_col2, insight_col3 = st.columns(3)

    insight_col1.metric("Average Error Rate", f'{summary_data["average_error_rate_percent"]}%')
    insight_col2.metric("Average Uptime", f'{summary_data["average_uptime_percent"]}%')
    insight_col3.metric(
        "Critical/Down Services",
        summary_data["critical_services"] + summary_data["down_services"]
    )

except requests.exceptions.ConnectionError:
    st.error(
        "Could not connect to the HealthOps backend API. "
        "Make sure FastAPI is running on http://127.0.0.1:8001"
    )
except Exception as error:
    st.error(f"An unexpected error occurred: {error}")

time.sleep(5)
st.rerun()