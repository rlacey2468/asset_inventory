import streamlit as st

from services.database_service import get_all_inventory


def require_login():

    if not st.session_state.get("logged_in"):

        st.error("Please log in first.")
        st.stop()


def require_role(allowed_roles):

    require_login()

    if st.session_state.role not in allowed_roles:

        st.error("You do not have permission to access this page.")
        st.stop()


def get_logged_in_user():

    return {
        "username": st.session_state.username,
        "role": st.session_state.role,
        "agency": st.session_state.agency
    }


def get_accessible_inventory():

    inventory = get_all_inventory()

    if st.session_state.role == "Admin":
        return inventory

    if st.session_state.role == "Viewer":

        return [
            device
            for device in inventory
            if device[4] == st.session_state.agency
        ]

    return []


def show_sidebar():

    st.sidebar.markdown("##  User")

    st.sidebar.write(f"**Username:** {st.session_state.username}")
    st.sidebar.write(f"**Role:** {st.session_state.role}")

    if st.session_state.role == "Viewer":
        st.sidebar.write(f"**Agency:** {st.session_state.agency}")

    st.sidebar.divider()

    if st.sidebar.button("Logout"):

        st.session_state.clear()

        st.rerun()