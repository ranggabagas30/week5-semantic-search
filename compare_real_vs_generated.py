"""Run the queries.md test set against both collections side by side.

Requires index.py (builds 'docs' from corpus/) and index_real.py (builds
'docs_real' from corpus/real/) to have been run first.
"""
from qdrant_client import QdrantClient, models

model_name = "intfloat/multilingual-e5-large"  # keep in sync with index.py's model_name

# Keep in sync with queries.md
QUERIES = [
    "purchase order packaging materials",
    "warehouse rent courier fees",
    "wrong colour blue black exchange",
    "database connection pool exhausted",
    "annual leave request family trip",
    "customer still has not sent the money",
    "website down customers cannot access",
    "supplier increasing prices",
    "money reimbursed to buyer",
    "employee resignation handover",
]

client = QdrantClient(path="./qdrant_data")
collections = {c.name for c in client.get_collections().collections}

for name in ("docs", "docs_real"):
    if name not in collections:
        print(f"Collection '{name}' not found — run "
              f"{'index.py' if name == 'docs' else 'index_real.py'} first.")

if not {"docs", "docs_real"} <= collections:
    raise SystemExit(1)

print(f"{'query':45s} {'generated (docs)':38s} {'real (docs_real)':38s}")
print("-" * 121)
for q in QUERIES:
    query_vector = models.Document(text=f"query: {q}", model=model_name)
    gen = client.query_points(collection_name="docs", query=query_vector, limit=1).points
    real = client.query_points(collection_name="docs_real", query=query_vector, limit=1).points
    g = f"{gen[0].score:.3f}  {gen[0].payload['metadata']['source']}" if gen else "(none)"
    r = f"{real[0].score:.3f}  {real[0].payload['metadata']['source']}" if real else "(none)"
    print(f"{q:45s} {g:38s} {r:38s}")
