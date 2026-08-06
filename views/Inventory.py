import streamlit as st
import pandas as pd


if not st.session_state.get("logged_in"):

    st.error("Please log in first.")

    st.stop()

from services.database_service import (
    get_all_inventory,
    get_inventory_by_id
)

if st.session_state.role == "Admin":

    inventory = get_all_inventory()

else:

    inventory = [
        device
        for device in get_all_inventory()
        if device[4] == st.session_state.agency
    ]



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

st.title("IoT Asset Inventory")

# -----------------------------
# Filters
# -----------------------------
filter1, filter2, filter3, filter4 = st.columns(4)

with filter1:
    manufacturers = ["All"] + sorted(
        df["Manufacturer"].dropna().unique().tolist()
    )

    selected_manufacturer = st.selectbox(
        "Manufacturer",
        manufacturers
    )

with filter2:
    models = ["All"] + sorted(
        df["Model"].dropna().unique().tolist()
    )

    selected_model = st.selectbox(
        "Model",
        models
    )

with filter3:
    agencies = ["All"] + sorted(
        df["Agency"].dropna().unique().tolist()
    )

    selected_agency = st.selectbox(
        "Agency",
        agencies
    )

with filter4:
    selected_criticality = st.selectbox(
        "Criticality",
        ["All", "Low", "Medium", "High", "Critical"]
    )

# -----------------------------
# Apply Filters
# -----------------------------
if selected_manufacturer != "All":
    df = df[df["Manufacturer"] == selected_manufacturer]

if selected_model != "All":
    df = df[df["Model"] == selected_model]

if selected_agency != "All":
    df = df[df["Agency"] == selected_agency]

if selected_criticality != "All":
    df = df[df["Criticality"] == selected_criticality]

# -----------------------------
# Metrics
# -----------------------------
metric1, metric2, metric3 = st.columns(3)

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

st.divider()

# -----------------------------
# Inventory Table
# -----------------------------
st.subheader("Inventory")

st.dataframe(
    df,
    width="stretch",
    hide_index=True
)

df = df.sort_values(
    by=["Manufacturer", "Model"]
)

if df.empty:
    st.warning("No devices match the selected filters.")
else:
    st.divider()
    st.subheader("Device Details")

    device_options = {
        f"{row['Manufacturer']} - {row['Model']} ({row['Agency']})": row["ID"]
        for _, row in df.iterrows()
    }

    selected_label = st.selectbox(
        "Select Device",
        list(device_options.keys())
    )

    selected_device = device_options[selected_label]

    device = get_inventory_by_id(selected_device)

    if device:
        info1, info2 = st.columns(2)

        with info1:
            st.info(f"""
**Manufacturer:** {device[1]}

**Model:** {device[2]}

**Firmware Version:** {device[3]}
""")

        with info2:
            st.info(f"""
**Agency:** {device[4]}

**Criticality:** {device[5]}

**Created At:** {device[6]}
""")