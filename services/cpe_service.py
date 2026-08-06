import requests

BASE_URL = "https://services.nvd.nist.gov/rest/json/cpes/2.0"


def search_cpes(manufacturer, model, firmware):

    # Search with firmware first, then without
    if firmware and firmware.strip().upper() != "TBD":
        keywords = [
            f"{manufacturer} {model} {firmware}",
            f"{manufacturer} {model}"
        ]
    else:
        keywords = [
            f"{manufacturer} {model}"
        ]

    for keyword in keywords:

        print(f"Searching for: {keyword}")

        response = requests.get(
            BASE_URL,
            params={
                "keywordSearch": keyword
            },
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if not data.get("products"):
            continue

        products = []

        for item in data["products"]:

            cpe = item["cpe"]

            cpe_name = cpe.get("cpeName")

            if not cpe_name:
                continue

            parts = cpe_name.split(":")

            if len(parts) < 6:
                continue

            type_map = {
                "a": "Application",
                "o": "Operating System",
                "h": "Hardware"
            }

            cpe_type = type_map.get(parts[2], parts[2])

            vendor = parts[3].replace("_", " ").title()
            product = parts[4].replace("_", " ").title()
            version = parts[5]

            if version == "-":
                version = "Unknown"

            title = (
                f"{vendor} {product} "
                f"({cpe_type}) - Version: {version}"
            )

            products.append({
                "title": title,
                "cpeName": cpe_name
            })

        if products:
            return products

    return []