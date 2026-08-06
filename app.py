import streamlit as st

from services.auth_service import login

st.set_page_config(
    page_title="IoT Asset Security Manager",
    page_icon="🛡️",
    layout="wide"
)

# -------------------------
# Login Screen
# -------------------------
if not st.session_state.get("logged_in", False):

    st.title("Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = login(username, password)

        if user:

            st.session_state.logged_in = True
            st.session_state.username = user[0]
            st.session_state.role = user[1]
            st.session_state.agency = user[2]

            st.rerun()

        else:

            st.error("Invalid username or password.")

    st.stop()

# -------------------------
# Navigation
# -------------------------
role = st.session_state.role

if role == "Admin":

    pages = [
        st.Page("views/dashboard.py", title="Dashboard"),
        st.Page("views/inventory.py", title="Inventory"),
        st.Page("views/manage_inventory.py", title="Manage Inventory"),
        st.Page("views/csv_import.py", title="CSV Import"),
        st.Page("views/vulnerability_lookup.py", title="Vulnerability Lookup"),
    ]

elif role == "Viewer":

    pages = [
        st.Page("views/inventory.py", title="Inventory", ),
        st.Page("views/vulnerability_lookup.py", title="Vulnerability Lookup"),
    ]

elif role == "Analyst":

    pages = [
        st.Page("views/dashboard.py", title="Dashboard"),
    ]

else:

    st.error("Unknown user role.")
    st.stop()

navigation = st.navigation(pages)

navigation.run()