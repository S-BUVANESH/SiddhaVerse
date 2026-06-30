from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import inspect

def check():
    client = QdrantClient(location=":memory:")
    client.create_collection(
        collection_name="test_col",
        vectors_config=VectorParams(size=3, distance=Distance.COSINE)
    )
    
    client.upsert(
        collection_name="test_col",
        points=[
            PointStruct(id=1, vector=[0.1, 0.2, 0.3], payload={"text": "hello"}),
            PointStruct(id=2, vector=[0.9, 0.8, 0.7], payload={"text": "world"})
        ]
    )
    
    print("Inspect query_points method:")
    sig = inspect.signature(client.query_points)
    print(sig)
    
    # Try query_points
    res = client.query_points(
        collection_name="test_col",
        query=[0.1, 0.2, 0.3],
        limit=2
    )
    print("\nQuery points results:")
    for hit in res.points:
        print(f"id: {hit.id}, score: {hit.score}, payload: {hit.payload}")

if __name__ == "__main__":
    check()
