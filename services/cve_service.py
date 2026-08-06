import requests

BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def get_cves(cpe_name):

    response = requests.get(
        BASE_URL,
        params={
            "cpeName": cpe_name
        },
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    cves = []

    for item in data.get("vulnerabilities", []):

        cve = item["cve"]

        metrics = cve.get("metrics", {})

        severity = "N/A"
        score = "N/A"

        if "cvssMetricV31" in metrics:

            metric = metrics["cvssMetricV31"][0]

            severity = metric["cvssData"]["baseSeverity"]
            score = metric["cvssData"]["baseScore"]

        elif "cvssMetricV30" in metrics:

            metric = metrics["cvssMetricV30"][0]

            severity = metric["cvssData"]["baseSeverity"]
            score = metric["cvssData"]["baseScore"]

        elif "cvssMetricV2" in metrics:

            metric = metrics["cvssMetricV2"][0]

            severity = metric.get("baseSeverity", "N/A")
            score = metric["cvssData"]["baseScore"]

        description = ""

        for desc in cve.get("descriptions", []):

            if desc["lang"] == "en":
                description = desc["value"]
                break

        cves.append({

            "id": cve["id"],

            "severity": severity,

            "score": score,

            "published": cve["published"],

            "description": description

        })

    return cves