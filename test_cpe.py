from services.cpe_service import search_cpes

results = search_cpes(
    "Cisco",
    "IR1101",
    "17.9.2"
)

for result in results:
    print(result)