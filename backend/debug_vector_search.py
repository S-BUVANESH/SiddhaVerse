import os
import sys
import uuid
from qdrant_client import QdrantClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from backend.app.embeddings import EmbeddingGenerator

def debug():
    sys.stdout.reconfigure(encoding='utf-8')
    qclient = QdrantClient(path=r"d:\Siddha_Wisdom\qdrant_db")
    generator = EmbeddingGenerator()
    
    query = "நினைப்பதொன்று கண்டேன்"
    query_vector = generator.embed_queries([query])[0]
    
    res = qclient.query_points(
        collection_name="siddhaverse_documents",
        query=query_vector,
        limit=50
    )
    
    print(f"=== Debugging Vector Search for Query: '{query}' ===")
    print("Top 20 results:")
    for idx, hit in enumerate(res.points[:20]):
        payload = hit.payload
        print(f"  {idx+1}. score={hit.score:.4f} | id={payload['document_id']} | title={payload['title']}")
        
    # Check if target is in the returned list
    target_id = "sivavakkiyar_pm_0616"
    target_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, target_id))
    print(f"\nChecking target document: '{target_id}' (UUID: {target_uuid})")
    
    exists = qclient.retrieve(collection_name="siddhaverse_documents", ids=[target_uuid])
    if exists:
        point = exists[0]
        print(f"  Found in Qdrant! Payload: {point.payload}")
        # Let's see what score it would get by computing cosine similarity
        import numpy as np
        vector = point.vector
        if vector is None:
            # Re-fetch with vectors
            point_with_vec = qclient.retrieve(collection_name="siddhaverse_documents", ids=[target_uuid], with_vectors=True)[0]
            vector = point_with_vec.vector
            
        dot_product = np.dot(query_vector, vector)
        print(f"  Manually computed cosine score with query: {dot_product:.6f}")
    else:
        print("  NOT found in Qdrant collection!")

if __name__ == "__main__":
    debug()
