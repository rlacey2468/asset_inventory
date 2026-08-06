import streamlit as st
import pandas as pd
import plotly.express as px

from services.auth_helper import (
    require_role,
    show_sidebar
)

require_role(
    ["Admin", "Analyst"]
)

show_sidebar()

from services.database_service import get_all_inventory

st.set_page_config(
    page_title="IoT Security Dashboard",
    layout="wide"
)


st.title("IoT Security Dashboard")

# ----------------------------------
# Load Inventory
# ----------------------------------
inventory = get_all_inventory()

df = pd.DataFrame(
    inventory,
    columns=[
        "ID",
        "Manufacturer",
        "Model",
        "Firmware Version",
        "Agency",
        "Criticality",
        "Created At"
    ]
)

# ----------------------------------
# Dashboard Metrics
# ----------------------------------
metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    "Devices",
    len(df)
)

metric2.metric(
    "Agencies",
    df["Agency"].nunique()
)

metric3.metric(
    "High/Critical",
    len(
        df[
            df["Criticality"].isin(
                ["High", "Critical"]
            )
        ]
    )
)

metric4.metric(
    "Missing Firmware",
    len(
        df[
            df["Firmware Version"].isin(
                ["", "TBD"]
            )
        ]
    )
)

st.divider()

# ----------------------------------
# Devices by Agency
# ----------------------------------
agency_counts = (
    df["Agency"]
    .value_counts()
    .reset_index()
)

agency_counts.columns = [
    "Agency",
    "Devices"
]

agency_fig = px.bar(
    agency_counts,
    x="Agency",
    y="Devices",
    title="Devices by Agency"
)

# ----------------------------------
# Criticality Distribution
# ----------------------------------
criticality = (
    df["Criticality"]
    .value_counts()
    .reset_index()
)

criticality.columns = [
    "Criticality",
    "Count"
]

criticality_fig = px.pie(
    criticality,
    names="Criticality",
    values="Count",
    title="Criticality Distribution"
)

# ----------------------------------
# Top Manufacturers
# ----------------------------------
manufacturers = (
    df["Manufacturer"]
    .value_counts()
    .head(10)
    .reset_index()
)

manufacturers.columns = [
    "Manufacturer",
    "Devices"
]

manufacturer_fig = px.bar(
    manufacturers,
    x="Manufacturer",
    y="Devices",
    title="Top Manufacturers"
)

# ----------------------------------
# Firmware Status
# ----------------------------------
firmware = pd.DataFrame({
    "Status": [
        "Present",
        "Missing"
    ],
    "Count": [
        len(
            df[
                ~df["Firmware Version"].isin(
                    ["", "TBD"]
                )
            ]
        ),
        len(
            df[
                df["Firmware Version"].isin(
                    ["", "TBD"]
                )
            ]
        )
    ]
})

firmware_fig = px.pie(
    firmware,
    names="Status",
    values="Count",
    title="Firmware Status"
)

# ----------------------------------
# Charts Row 1
# ----------------------------------
left, right = st.columns(2)

with left:

    st.plotly_chart(
        agency_fig,
        width="stretch"
    )

with right:

    st.plotly_chart(
        criticality_fig,
        width="stretch"
    )

# ----------------------------------
# Charts Row 2
# ----------------------------------
left, right = st.columns(2)

with left:

    st.plotly_chart(
        manufacturer_fig,
        width="stretch"
    )

with right:

    st.plotly_chart(
        firmware_fig,
        width="stretch"
    )

# ----------------------------------
# High Risk Devices
# ----------------------------------
st.divider()

st.subheader("🚨 High Risk Devices")

high_risk = df[
    df["Criticality"].isin(
        ["High", "Critical"]
    )
].copy()

severity_order = {
    "Critical": 2,
    "High": 1
}

high_risk["Sort"] = high_risk["Criticality"].map(
    severity_order
)

high_risk = (
    high_risk
    .sort_values(
        "Sort",
        ascending=False
    )
    .drop(columns="Sort")
)

if high_risk.empty:

    st.success(
        "No High or Critical devices found."
    )

else:

    st.dataframe(
        high_risk[
            [
                "Manufacturer",
                "Model",
                "Firmware Version",
                "Agency",
                "Criticality"
            ]
        ],
        width="stretch",
        hide_index=True
    )