"""Index corpus/real/ into a separate Qdrant collection for benchmarking.

Companion to index.py (Step 2 of the trainee guide) — same pattern, but
sources corpus/real/ into its own collection so it can be compared against
the generated corpus without disturbing it. Run index.py first, then this.
"""
from pathlib import Path

from qdrant_client import QdrantClient, models

model_name = "intfloat/multilingual-e5-large"  # keep in sync with index.py's model_name
client = QdrantClient(path="./qdrant_data")
docs: list[str] = []
meta: list[dict] = []
ids: list[int] = []

for n, p in enumerate(sorted(Path("corpus/real").glob("*.*"))):
    if p.name == "README.md":
        continue
    text = p.read_text(errors="ignore")
    docs.append(text[:2000])
    meta.append({"source": p.name, "type": p.suffix.lstrip(".")})
    ids.append(n)

client.create_collection(
    collection_name="docs_real",
    vectors_config=models.VectorParams(
        size=client.get_embedding_size(model_name), distance=models.Distance.COSINE
    ),
)
payload = [{"document": doc, "metadata": m} for doc, m in zip(docs, meta)]
client.upload_collection(
    collection_name="docs_real",
    vectors=[models.Document(text=f"passage: {doc}", model=model_name) for doc in docs],
    payload=payload,
    ids=ids,
)
print(f"indexed {len(docs)} real documents into collection 'docs_real'")
