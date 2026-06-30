import os
import sys
import sqlite3
from sentence_transformers import CrossEncoder

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def debug():
    sys.stdout.reconfigure(encoding='utf-8')
    cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    
    # Fetch target documents
    db_path = r"d:\Siddha_Wisdom\siddhaverse.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT document_id, title, search_text FROM documents WHERE document_id IN ('sivavakkiyar_pm_0616', 'classic_thirumandiram')")
    docs = {r[0]: {"title": r[1], "text": r[2]} for r in cur.fetchall()}
    conn.close()
    
    test_cases = [
        ("pranayamam", "classic_thirumandiram"),
        ("pranayamam", "sivavakkiyar_pm_0616"),
        ("breath retention", "classic_thirumandiram"),
        ("breath retention", "sivavakkiyar_pm_0616"),
    ]
    
    print("=== Debugging Cross-Encoder Scores ===")
    for query, doc_id in test_cases:
        if doc_id in docs:
            doc = docs[doc_id]
            score = cross_encoder.predict([(query, doc["text"])])[0]
            print(f"Query: '{query}' | Doc ID: '{doc_id}' | Title: '{doc['title']}'")
            print(f"  Score: {score:.4f} (Pruned if < 0.35)")
            # print(f"  Text preview: {doc['text'][:150]}...")
            print("-" * 50)
            
if __name__ == "__main__":
    debug()
