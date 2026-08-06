import streamlit as st

from services.auth_helper import (
    require_role,
    show_sidebar
)

require_role(["Admin"])

show_sidebar()

from services.database_service import (
    get_all_inventory,
    get_inventory_by_id,
    add_inventory,
    update_inventory,
    delete_inventory
)

st.title("Manage Inventory")

# ---------------------------------
# Tabs
# ---------------------------------
add_tab, edit_tab, delete_tab = st.tabs(
    ["Add Device", "Edit Device", "Delete Device"]
)

# =================================
# Add Device
# =================================
with add_tab:

    with st.form("add_device"):

        manufacturer = st.text_input("Manufacturer")

        model = st.text_input("Model")

        firmware = st.text_input("Firmware Version")

        agency = st.text_input("Agency")

        criticality = st.selectbox(
            "Criticality",
            ["Low", "Medium", "High", "Critical"]
        )

        submitted = st.form_submit_button("Add Device")

        if submitted:

            try:

                add_inventory(
                    manufacturer,
                    model,
                    firmware,
                    agency,
                    criticality
                )

                st.success("Device added successfully!")

            except ValueError as e:

                st.error(str(e))

# =================================
# Edit Device
# =================================
with edit_tab:

    inventory = get_all_inventory()

    device_options = {
        f"{row[1]} - {row[2]} ({row[4]})": row[0]
        for row in inventory
    }

    selected = st.selectbox(
        "Select Device",
        list(device_options.keys()),
        key="edit_device"
    )

    device = get_inventory_by_id(
        device_options[selected]
    )

    with st.form("edit_device_form"):

        manufacturer = st.text_input(
            "Manufacturer",
            value=device[1]
        )

        model = st.text_input(
            "Model",
            value=device[2]
        )

        firmware = st.text_input(
            "Firmware Version",
            value=device[3]
        )

        agency = st.text_input(
            "Agency",
            value=device[4]
        )

        criticality = st.selectbox(
            "Criticality",
            ["Low", "Medium", "High", "Critical"],
            index=["Low", "Medium", "High", "Critical"].index(device[5])
        )

        submitted = st.form_submit_button("Update Device")

        if submitted:

            try:

                update_inventory(
                    device[0],
                    manufacturer,
                    model,
                    firmware,
                    agency,
                    criticality
                )

                st.success("Device updated successfully!")

            except ValueError as e:

                st.error(str(e))

# =================================
# Delete Device
# =================================
with delete_tab:

    inventory = get_all_inventory()

    device_options = {
        f"{row[1]} - {row[2]} ({row[4]})": row[0]
        for row in inventory
    }

    selected = st.selectbox(
        "Select Device",
        list(device_options.keys()),
        key="delete_device"
    )

    device = get_inventory_by_id(
        device_options[selected]
    )

    st.warning(
        f"Are you sure you want to delete **{device[1]} - {device[2]}**?"
    )

    confirm = st.checkbox(
        "I understand this action cannot be undone."
    )

    if confirm:

        if st.button("Delete Device"):

            try:

                delete_inventory(device[0])

                st.success("Device deleted successfully!")

            except ValueError as e:

                st.error(str(e))