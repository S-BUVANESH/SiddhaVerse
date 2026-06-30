import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from backend.app.repositories import SQLiteDocumentRepository

def debug():
    repo = SQLiteDocumentRepository()
    q = "pranayamam"
    print(f"=== Debugging Hybrid Search for Query: '{q}' ===")
    
    # 1. Fetch lexical and vector search candidates
    lexical_results, _ = repo.search_lexical(
        q=q, doc_type="all", work="all", author="all",
        entity_id=None, page=1, per_page=30
    )
    vector_results, _ = repo.search_vector(
        q=q, doc_type="all", work="all", author="all",
        entity_id=None, page=1, per_page=30
    )
    
    print(f"Lexical Results count: {len(lexical_results)}")
    for idx, d in enumerate(lexical_results[:5]):
        print(f"  Lexical {idx+1}. id={d['document_id']} | title={d['title']}")
        
    print(f"Vector Results count: {len(vector_results)}")
    for idx, d in enumerate(vector_results[:5]):
        print(f"  Vector {idx+1}. id={d['document_id']} | title={d['title']}")
        
    # 2. RRF
    rrf_scores = {}
    doc_map = {}
    for rank, doc in enumerate(lexical_results, 1):
        doc_id = doc["document_id"]
        doc_map[doc_id] = doc
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (60.0 + rank))
    for rank, doc in enumerate(vector_results, 1):
        doc_id = doc["document_id"]
        doc_map[doc_id] = doc
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (60.0 + rank))
        
    sorted_doc_ids = sorted(rrf_scores.keys(), key=lambda k: rrf_scores[k], reverse=True)
    print(f"\nTop 15 sorted RRF IDs:")
    for idx, d_id in enumerate(sorted_doc_ids[:15]):
        lex_rank = next((r for r, d in enumerate(lexical_results, 1) if d["document_id"] == d_id), None)
        vec_rank = next((r for r, d in enumerate(vector_results, 1) if d["document_id"] == d_id), None)
        print(f"  {idx+1}. id={d_id} | RRF={rrf_scores[d_id]:.5f} | LexRank={lex_rank} | VecRank={vec_rank}")
        
    # 3. Cross encoder
    top_candidates = [doc_map[d_id] for d_id in sorted_doc_ids[:15]]
    from sentence_transformers import CrossEncoder
    cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    pairs = [(q, doc.get("search_text") or doc.get("tamil_text") or "") for doc in top_candidates]
    scores = cross_encoder.predict(pairs)
    
    print("\nReranking & Pruning Details:")
    max_rrf = max(rrf_scores.values()) if rrf_scores else 1.0
    for idx, (doc, score) in enumerate(zip(top_candidates, scores)):
        import math
        prob = 1.0 / (1.0 + math.exp(-score))
        doc_id = doc["document_id"]
        norm_rrf = rrf_scores[doc_id] / max_rrf
        combined_score = 0.5 * prob + 0.5 * norm_rrf
        
        lex_rank = next((r for r, d in enumerate(lexical_results, 1) if d["document_id"] == doc_id), None)
        vec_rank = next((r for r, d in enumerate(vector_results, 1) if d["document_id"] == doc_id), None)
        is_top_lex = (lex_rank is not None and lex_rank <= 3)
        is_top_vec = (vec_rank is not None and vec_rank <= 3)
        
        final_score = combined_score
        if is_top_lex or is_top_vec:
            final_score = max(combined_score, 0.45)
            
        print(f"  Candidate {idx+1}. id={doc_id} | RawCE={score:.4f} | Prob={prob:.4f} | NormRRF={norm_rrf:.4f} | Combined={combined_score:.4f} | Final={final_score:.4f} | Keep={final_score >= 0.35}")

if __name__ == "__main__":
    debug()
