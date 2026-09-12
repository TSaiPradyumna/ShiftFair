"""
Run: python3 seed_and_search.py
Requires: pip install opensearch-py
"""
from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_compress=True,
    use_ssl=False,
    verify_certs=False,
)

INDEX = "shift_history"

sample_shifts = [
    {"employee_id": "E001", "date": "2026-09-01", "shift_type": "night", "notes": "covered for E003"},
    {"employee_id": "E001", "date": "2026-09-03", "shift_type": "night", "notes": "regular shift"},
    {"employee_id": "E002", "date": "2026-09-02", "shift_type": "day", "notes": "regular shift"},
    {"employee_id": "E003", "date": "2026-09-05", "shift_type": "night", "notes": "requested swap, denied - rest hours"},
]

def seed():
    if not client.indices.exists(INDEX):
        client.indices.create(INDEX)
    for i, doc in enumerate(sample_shifts):
        client.index(index=INDEX, id=i, body=doc, refresh=True)
    print(f"Seeded {len(sample_shifts)} shift records into '{INDEX}'")

def search_by_employee(employee_id):
    query = {"query": {"match": {"employee_id": employee_id}}}
    res = client.search(index=INDEX, body=query)
    print(f"\nResults for employee_id={employee_id}:")
    for hit in res["hits"]["hits"]:
        print(" ", hit["_source"])

if __name__ == "__main__":
    seed()
    search_by_employee("E001")
