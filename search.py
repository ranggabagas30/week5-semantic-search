import sys
import argparse
from qdrant_client import QdrantClient, models

def search(query: str, doc_type: str | None = None): 
    fit = None 
    if doc_type: 
        fit = models.Filter(must=[models.FieldCondition(key="metadata.type", match=models.MatchValue(value=doc_type))])
    return client.query_points(collection_name="docs", query=models.Document(text=query, model=model), query_filter=fit, limit=5).points
    
model="BAAI/bge-small-en"
client = QdrantClient(path="./qdrant_data")

parser = argparse.ArgumentParser()
parser.add_argument("--type", dest="doc_type", default=None)
parser.add_argument("query", nargs="+")
args = parser.parse_args()

hits = search(" ".join(args.query), args.doc_type)
for h in hits: 
    print(f"{h.score:.3f}  {h.payload["metadata"]["source"]}", "\n")
    print(" ", h.payload["document"][:100].replace("\n", ""), "\n\n")