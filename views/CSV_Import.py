import streamlit as st

from services.csv_import import import_inventory

from services.auth_helper import (
    require_role,
    show_sidebar
)

require_role(["Admin"])

show_sidebar()

st.title("CSV Import")

st.write(
    "Upload a CSV file to import IoT inventory into the database."
)

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    st.success(f"Selected file: {uploaded_file.name}")

    if st.button("Import Inventory"):

        try:

            imported, failed, errors = import_inventory(uploaded_file)

            st.success(
                f"Successfully imported {imported} devices."
            )

            if failed > 0:
                st.warning(
                    f"{failed} rows could not be imported."
                )

            st.subheader("Import Errors")

            for error in errors:
                st.error(error)

        except Exception as e:

            st.error(str(e))
