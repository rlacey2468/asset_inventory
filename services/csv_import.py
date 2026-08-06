import pandas as pd
from services.database_service import add_inventory

REQUIRED_COLUMNS = [
    "Manufacturer",
    "Model",
    "Firmware Version",
    "Agency",
    "Criticality"
]

def import_inventory(csv_file):

    df = pd.read_csv(csv_file)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(missing)}"
        )

    imported = 0
    failed = 0
    errors = []

    for index, row in df.iterrows():

        try:

            add_inventory(
                manufacturer=row["Manufacturer"],
                model=row["Model"],
                firmware=row["Firmware Version"],
                agency=row["Agency"],
                criticality=row["Criticality"]
            )

            imported += 1

        except ValueError as e:

            failed += 1

            errors.append(
                f"Row {index + 2}: {e}"
            )

    return imported, failed, errors