from pathlib import Path 
from qdrant_client import QdrantClient, models
model_name = "BAAI/bge-small-en"
client = QdrantClient(path="./qdrant_data")
docs, meta, ids = [], [], []
for n, p in enumerate(sorted(Path("corpus").glob("*.*"))):
    print(f"n: {n}, reading {p.name}")
    text = p.read_text(errors="ignore")
    docs.append(text[:2000]) # whole doc for now
    meta.append({"source": p.name, "type": p.suffix.lstrip(".")})
    ids.append(n)
    
print(f"ids: {ids}")
client.create_collection(
    collection_name="docs",
    vectors_config=models.VectorParams(size=client.get_embedding_size(model_name), distance=models.Distance.COSINE),
)
metadata_with_docs = [
    {"document": doc, "metadata": m} for doc, m in zip(docs, meta)
]
client.upload_collection(
    collection_name="docs",
    vectors=[models.Document(text=doc, model=model_name) for doc in docs],
    payload=metadata_with_docs,
    ids=ids,
)
print(f"indexed {len(docs)} documents")
