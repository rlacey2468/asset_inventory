from services.cve_service import get_cves

cves = get_cves(
    "cpe:2.3:h:cisco:ir1101:-:*:*:*:*:*:*:*"
)

print(f"Found {len(cves)} CVEs\n")

for cve in cves[:5]:

    print(cve["id"])
    print(cve["severity"])
    print(cve["score"])
    print(cve["published"])
    print(cve["description"])
    print("-" * 60)