import sqlite3
import random
import re
import os
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
from backend.app.database import get_db_connection, row_to_dict

_embedding_generator = None
_qdrant_client = None
_cross_encoder = None
_cross_encoder_name = None

class BaseDocumentRepository(ABC):
    @abstractmethod
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def search_lexical(self, q: str, doc_type: str = "all", work: str = "all",
                       author: str = "all", entity_id: str = None, category: str = None,
                       page: int = 1, per_page: int = 20, sort: str = "relevance") -> Tuple[List[Dict[str, Any]], int]:
        pass

    @abstractmethod
    def search_vector(self, q: str, doc_type: str = "all", work: str = "all",
                      author: str = "all", entity_id: str = None, page: int = 1,
                      per_page: int = 20) -> Tuple[List[Dict[str, Any]], int]:
        pass

    @abstractmethod
    def search_hybrid(self, q: str, doc_type: str = "all", work: str = "all",
                      author: str = "all", entity_id: str = None, page: int = 1,
                      per_page: int = 20) -> Tuple[List[Dict[str, Any]], int]:
        pass

    @abstractmethod
    def get_entity_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_plant_by_id(self, plant_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_siddhar_by_id(self, siddhar_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_work_by_id(self, work_id: str, collection: str = "all", page: int = 1, per_page: int = 50) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_formulation_by_id(self, formulation_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def list_collections(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_random_verse(self, work: str = "all", entity_id: str = None) -> Optional[Dict[str, Any]]:
        pass


class SQLiteDocumentRepository(BaseDocumentRepository):
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM documents WHERE document_id = ?;", (doc_id,))
            row = cursor.fetchone()
            if not row:
                return None
            doc = row_to_dict(row)

            # Retrieve adjacent verses if the document is a verse
            if doc.get("doc_type") == "verse":
                work = doc.get("source_work")
                vnum_str = doc.get("verse_number")
                if work and vnum_str and vnum_str.isdigit():
                    vnum = int(vnum_str)
                    cursor.execute("""
                        SELECT document_id FROM documents 
                        WHERE source_work = ? AND CAST(verse_number AS INTEGER) = ?;
                    """, (work, vnum - 1))
                    prev_row = cursor.fetchone()

                    cursor.execute("""
                        SELECT document_id FROM documents 
                        WHERE source_work = ? AND CAST(verse_number AS INTEGER) = ?;
                    """, (work, vnum + 1))
                    next_row = cursor.fetchone()

                    doc["adjacent"] = {
                        "previous": prev_row[0] if prev_row else None,
                        "next": next_row[0] if next_row else None
                    }
            return doc

    def search_lexical(self, q: str, doc_type: str = "all", work: str = "all",
                       author: str = "all", entity_id: str = None, category: str = None,
                       page: int = 1, per_page: int = 20, sort: str = "relevance") -> Tuple[List[Dict[str, Any]], int]:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Compile parameters and build SQL
            params = []
            where_clauses = []

            # Full-text query match
            if q and q.strip():
                # SQLite FTS5 MATCH clause
                where_clauses.append("documents.document_id IN (SELECT document_id FROM documents_fts WHERE documents_fts MATCH ?)")
                
                # Load synonym map and suffix stripping rules
                syn_path = r"d:\Siddha_Wisdom\synonym_map.json"
                synonyms = {}
                if os.path.exists(syn_path):
                    with open(syn_path, "r", encoding="utf-8") as f:
                        synonyms = json.load(f).get("synonyms", {})
                        
                suf_path = r"d:\Siddha_Wisdom\suffix_rules.json"
                suffix_rules = []
                if os.path.exists(suf_path):
                    with open(suf_path, "r", encoding="utf-8") as f:
                        suffix_rules = json.load(f).get("rules", [])

                q_clean = q.strip().lower()
                terms = set()
                
                # 1. Match multi-word synonym phrases first
                for phrase, syn_list in list(synonyms.items()):
                    if " " in phrase and phrase in q_clean:
                        terms.update(syn_list)
                        terms.add(phrase)
                        q_clean = q_clean.replace(phrase, "")
                        
                # 2. Tokenize remaining words
                words = re.sub(r'[^a-zA-Z0-9\s\u0b80-\u0bff]', ' ', q_clean).split()
                for w in words:
                    if not w:
                        continue
                    terms.add(w)
                    
                    # Apply suffix stripping
                    stem = w
                    for rule in suffix_rules:
                        if w.endswith(rule["suffix"]) and rule["strip"] > 0:
                            stripped = w[:-rule["strip"]]
                            if len(stripped) >= 4:
                                stem = stripped
                                terms.add(stem)
                                break
                                
                    # Check synonyms for original word and stem
                    if w in synonyms:
                        terms.update(synonyms[w])
                    if stem in synonyms:
                        terms.update(synonyms[stem])
                
                # Wrap terms in double quotes with * suffix for prefix matching
                fts_terms = []
                for t in terms:
                    t_clean = re.sub(r'[^a-zA-Z0-9\s\u0b80-\u0bff]', ' ', t).strip()
                    if t_clean:
                        fts_terms.append(f'"{t_clean}"*')
                
                fts_query = " OR ".join(fts_terms) if fts_terms else "*"
                params.append(fts_query)

            if doc_type != "all" and doc_type:
                where_clauses.append("documents.doc_type = ?")
                params.append(doc_type)

            if work != "all" and work:
                where_clauses.append("documents.source_work = ?")
                params.append(work)

            if author != "all" and author:
                where_clauses.append("documents.author LIKE ?")
                params.append(f"%{author}%")

            if entity_id:
                # Matches JSON array string (e.g. contains '"entity_id"')
                where_clauses.append("documents.entity_ids LIKE ?")
                params.append(f'%"{entity_id}"%')

            # Execute filters
            where_sql = f" WHERE {' AND '.join(where_clauses)}" if where_clauses else ""

            # Count total matching records
            count_sql = f"SELECT COUNT(*) FROM documents {where_sql};"
            cursor.execute(count_sql, params)
            total = cursor.fetchone()[0]

            # Sorting strategies
            if sort == "verse_number":
                order_sql = "ORDER BY CAST(documents.verse_number AS INTEGER) ASC"
            elif sort == "work":
                order_sql = "ORDER BY documents.source_work ASC, CAST(documents.verse_number AS INTEGER) ASC"
            elif sort == "author":
                order_sql = "ORDER BY documents.author ASC"
            else:
                # Default is relevance. If FTS is active, use BM25 score. Otherwise fallback to ID.
                if q and q.strip():
                    # JOIN on FTS to get rank
                    order_sql = "ORDER BY rank"
                else:
                    order_sql = "ORDER BY documents.document_id ASC"

            # Pagination
            limit = per_page
            offset = (page - 1) * per_page
            
            # Form final query
            if q and q.strip():
                # Join FTS for BM25 ranking
                query_sql = f"""
                SELECT documents.*, documents_fts.rank 
                FROM documents 
                JOIN documents_fts ON documents.document_id = documents_fts.document_id
                {where_sql}
                {order_sql}
                LIMIT ? OFFSET ?;
                """
            else:
                query_sql = f"""
                SELECT documents.* 
                FROM documents 
                {where_sql}
                {order_sql}
                LIMIT ? OFFSET ?;
                """
            
            cursor.execute(query_sql, params + [limit, offset])
            rows = cursor.fetchall()
            results = [row_to_dict(row) for row in rows]
            return results, total

    def search_vector(self, q: str, doc_type: str = "all", work: str = "all",
                      author: str = "all", entity_id: str = None, page: int = 1,
                      per_page: int = 20) -> Tuple[List[Dict[str, Any]], int]:
        if not q or not q.strip():
            return [], 0
            
        from backend.app.embeddings import EmbeddingGenerator
        from qdrant_client import QdrantClient
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        
        global _embedding_generator, _qdrant_client
        if _embedding_generator is None:
            _embedding_generator = EmbeddingGenerator()
        if _qdrant_client is None:
            _qdrant_client = QdrantClient(path=r"d:\Siddha_Wisdom\qdrant_db")
            
        query_vector = _embedding_generator.embed_queries([q])[0]
        
        # Build Qdrant conditions matching the SQLite filter values
        conditions = []
        if doc_type != "all" and doc_type:
            conditions.append(FieldCondition(key="doc_type", match=MatchValue(value=doc_type)))
        if work != "all" and work:
            conditions.append(FieldCondition(key="source_work", match=MatchValue(value=work)))
        if author != "all" and author:
            conditions.append(FieldCondition(key="author", match=MatchValue(value=author)))
        if entity_id:
            conditions.append(FieldCondition(key="entity_ids", match=MatchValue(value=entity_id)))
            
        query_filter = Filter(must=conditions) if conditions else None
        
        limit = per_page
        offset = (page - 1) * per_page
        
        # Query Qdrant Points
        search_response = _qdrant_client.query_points(
            collection_name="siddhaverse_documents",
            query=query_vector,
            query_filter=query_filter,
            limit=limit,
            offset=offset
        )
        hits = search_response.points
        
        # Get total matching items for correct metadata pagination
        total_res = _qdrant_client.count(
            collection_name="siddhaverse_documents",
            count_filter=query_filter,
            exact=True
        )
        total = total_res.count
        
        # Resolve document IDs back to SQLite
        doc_ids = [hit.payload["document_id"] for hit in hits]
        results = []
        if doc_ids:
            placeholders = ",".join(["?"] * len(doc_ids))
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM documents WHERE document_id IN ({placeholders});", doc_ids)
                db_docs = {row[0]: row_to_dict(row) for row in cursor.fetchall()}
                
            for hit in hits:
                d_id = hit.payload["document_id"]
                if d_id in db_docs:
                    doc = db_docs[d_id]
                    doc["score"] = float(hit.score)
                    results.append(doc)
                    
        return results, total

    def search_hybrid(self, q: str, doc_type: str = "all", work: str = "all",
                      author: str = "all", entity_id: str = None, page: int = 1,
                      per_page: int = 20) -> Tuple[List[Dict[str, Any]], int]:
        if not q or not q.strip():
            return [], 0
            
        # 1. Fetch lexical and vector search candidates
        lexical_results, _ = self.search_lexical(
            q=q, doc_type=doc_type, work=work, author=author,
            entity_id=entity_id, page=1, per_page=30
        )
        vector_results, _ = self.search_vector(
            q=q, doc_type=doc_type, work=work, author=author,
            entity_id=entity_id, page=1, per_page=30
        )
        
        # 2. Fuse candidate lists using Reciprocal Rank Fusion (RRF)
        rrf_scores = {}
        doc_map = {}
        
        lex_weight = float(os.getenv("RRF_LEXICAL_WEIGHT", "1.0"))
        vec_weight = float(os.getenv("RRF_VECTOR_WEIGHT", "1.0"))
        
        for rank, doc in enumerate(lexical_results, 1):
            doc_id = doc["document_id"]
            doc_map[doc_id] = doc
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + lex_weight * (1.0 / (60.0 + rank))
            
        for rank, doc in enumerate(vector_results, 1):
            doc_id = doc["document_id"]
            doc_map[doc_id] = doc
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + vec_weight * (1.0 / (60.0 + rank))
            
        if not rrf_scores:
            return [], 0
            
        # Sort candidates by RRF score
        sorted_doc_ids = sorted(rrf_scores.keys(), key=lambda k: rrf_scores[k], reverse=True)
        total_unique = len(sorted_doc_ids)
        
        # Take top 15 candidates for expensive cross-encoder reranking
        top_candidates = [doc_map[d_id] for d_id in sorted_doc_ids[:15]]
        
        # 3. Rerank candidates using Cross-Encoder (if enabled)
        enable_reranker = os.getenv("ENABLE_RERANKER", "true").lower() == "true"
        
        if not enable_reranker:
            reranked_results = []
            max_rrf = max(rrf_scores.values()) if rrf_scores else 1.0
            if max_rrf == 0.0:
                max_rrf = 1.0
            for doc in top_candidates:
                doc_id = doc["document_id"]
                doc["score"] = rrf_scores[doc_id] / max_rrf
                reranked_results.append(doc)
        else:
            from sentence_transformers import CrossEncoder
            global _cross_encoder, _cross_encoder_name
            model_name = os.getenv("RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
            if _cross_encoder is None or _cross_encoder_name != model_name:
                print(f"Loading Cross-Encoder model: {model_name}...")
                _cross_encoder = CrossEncoder(model_name)
                _cross_encoder_name = model_name
                
            pairs = []
            for doc in top_candidates:
                # Reconstruct context text for reranker evaluation
                text = doc.get("search_text") or doc.get("tamil_text") or ""
                pairs.append((q, text))
                
            scores = _cross_encoder.predict(pairs)
            
            # 4. Filter by confidence threshold (>= 0.35) and sort using fused RRF + Cross-Encoder score
            reranked_results = []
            max_rrf = max(rrf_scores.values()) if rrf_scores else 1.0
            if max_rrf == 0.0:
                max_rrf = 1.0
            
            for doc, score in zip(top_candidates, scores):
                # Apply Sigmoid to cross-encoder raw logits
                import math
                prob = 1.0 / (1.0 + math.exp(-score))
                
                doc_id = doc["document_id"]
                norm_rrf = rrf_scores[doc_id] / max_rrf
                
                # Fused score (50% Cross-Encoder probability, 50% Normalized RRF rank)
                combined_score = 0.5 * prob + 0.5 * norm_rrf
                
                # Find original candidate ranks to protect highly relevant lexical/vector matches from pruning
                lexical_rank = next((r for r, d in enumerate(lexical_results, 1) if d["document_id"] == doc_id), None)
                vector_rank = next((r for r, d in enumerate(vector_results, 1) if d["document_id"] == doc_id), None)
                
                is_top_lexical = (lexical_rank is not None and lexical_rank <= 3)
                is_top_vector = (vector_rank is not None and vector_rank <= 3)
                
                # Safety gate: if the document was highly ranked in either search, guarantee it passes the 0.35 threshold
                if is_top_lexical or is_top_vector:
                    combined_score = max(combined_score, 0.45)
                    
                doc["score"] = combined_score
                
                if combined_score >= 0.35:
                    reranked_results.append(doc)
                    
        reranked_results.sort(key=lambda x: x["score"], reverse=True)
        
        # 5. Apply pagination over reranked results
        limit = per_page
        offset = (page - 1) * per_page
        paginated = reranked_results[offset : offset + limit]
        
        return paginated, total_unique

    def get_entity_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM entities WHERE entity_id = ?;", (entity_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return row_to_dict(row)

    def get_plant_by_id(self, plant_id: str) -> Optional[Dict[str, Any]]:
        doc = self.get_document_by_id(plant_id)
        if not doc or doc.get("doc_type") != "plant":
            return None
        
        # Build structure per API contract
        cf = doc.get("custom_fields") or {}
        return {
            "document_id":      doc.get("document_id"),
            "title":            doc.get("title"),
            "tamil_name":       cf.get("tamil") or doc.get("tamil_text"),
            "scientific_name":  cf.get("scientific"),
            "siddha_category":  cf.get("category") or "herbal",
            "description":      cf.get("uses") or doc.get("search_text"),
            "therapeutic_uses": cf.get("uses", "").split(", ") if cf.get("uses") else [],
            "copyright_status": doc.get("copyright_status"),
            "related_formulations": cf.get("related_formulations") or [],
            "verse_mentions":   cf.get("verse_mentions") or 0,
            "related_entity_id": doc.get("document_id")
        }

    def get_siddhar_by_id(self, siddhar_id: str) -> Optional[Dict[str, Any]]:
        doc = self.get_document_by_id(siddhar_id)
        if not doc or doc.get("doc_type") != "biography":
            return None
        cf = doc.get("custom_fields") or {}
        return {
            "document_id":   doc.get("document_id"),
            "name":          cf.get("name") or doc.get("author"),
            "tamil_name":    cf.get("tamil_name") or cf.get("tamil"),
            "period":        cf.get("period"),
            "primary_work":  cf.get("primary_work") or (cf.get("texts")[0] if cf.get("texts") else None),
            "philosophy":    cf.get("philosophy"),
            "description":   cf.get("biography") or doc.get("search_text"),
            "verse_count_in_corpus": cf.get("verse_count_in_corpus") or 0,
            "entity_id":     doc.get("document_id"),
            "copyright_status": doc.get("copyright_status"),
            "sample_verses": cf.get("sample_verses") or []
        }

    def get_work_by_id(self, work_id: str, collection: str = "all", page: int = 1, per_page: int = 50) -> Optional[Dict[str, Any]]:
        # Map work_id to exact source_work string
        work_mapping = {
            "thirumandiram": "Thirumandiram",
            "sivavakkiyam":  "Sivavakkiyam"
        }
        source_work = work_mapping.get(work_id.lower(), work_id)
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM documents WHERE source_work = ? AND doc_type = 'verse';", (source_work,))
            total_verses = cursor.fetchone()[0]
            if total_verses == 0:
                return None

            # Get collection distributions
            cursor.execute("""
                SELECT collection, COUNT(*) FROM documents 
                WHERE source_work = ? AND doc_type = 'verse' 
                GROUP BY collection;
            """, (source_work,))
            collections_list = [{"name": r[0], "verse_count": r[1]} for r in cursor.fetchall()]

            # Fetch paginated list of verses
            offset = (page - 1) * per_page
            where_clause = "WHERE source_work = ? AND doc_type = 'verse'"
            params = [source_work]
            if collection != "all":
                where_clause += " AND collection = ?"
                params.append(collection)
                
            cursor.execute(f"""
                SELECT document_id, verse_number, collection, tamil_text 
                FROM documents 
                {where_clause} 
                ORDER BY CAST(verse_number AS INTEGER) ASC 
                LIMIT ? OFFSET ?;
            """, params + [per_page, offset])
            
            verses = [{
                "document_id": r[0],
                "verse_number": r[1],
                "collection": r[2],
                "tamil_text": r[3]
            } for r in cursor.fetchall()]

            # Get metadata from first verse
            cursor.execute("SELECT author, script, language, source_url, copyright_status FROM documents WHERE source_work = ? LIMIT 1;", (source_work,))
            meta = cursor.fetchone()
            author, script, language, source_url, copyright_status = meta if meta else ("Unknown", "Tamil script", "Tamil", None, "public_domain")

            return {
                "work_id":       work_id,
                "title":         source_work,
                "author":        author,
                "period":        "c. 6th–7th century CE" if work_id.lower() == "thirumandiram" else "c. 9th–10th century CE",
                "language":      language,
                "script":        script,
                "total_verses_in_corpus": total_verses,
                "total_verses_in_work":   3000 if work_id.lower() == "thirumandiram" else 1000,
                "corpus_coverage_pct":    round((total_verses / (3000 if work_id.lower() == "thirumandiram" else 1000)) * 100, 2),
                "collections": collections_list,
                "verses": verses,
                "source_url": source_url,
                "copyright_status": copyright_status
            }

    def get_formulation_by_id(self, formulation_id: str) -> Optional[Dict[str, Any]]:
        doc = self.get_document_by_id(formulation_id)
        if not doc or doc.get("doc_type") != "formulation":
            return None
        cf = doc.get("custom_fields") or {}
        return {
            "document_id":   doc.get("document_id"),
            "title":         doc.get("title"),
            "type":          cf.get("category") or "herbal decoction",
            "ingredients":   cf.get("ingredients") or [],
            "indications":   cf.get("indications").split(", ") if isinstance(cf.get("indications"), str) else (cf.get("indications") or []),
            "preparation":   cf.get("method") or doc.get("search_text"),
            "source":        cf.get("source") or "AYUSH Ministry approved formulation",
            "copyright_status": doc.get("copyright_status")
        }

    def list_collections(self) -> Dict[str, Any]:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Count works
            cursor.execute("SELECT source_work, COUNT(*) FROM documents WHERE doc_type = 'verse' GROUP BY source_work;")
            works = [{"id": r[0].lower(), "title": r[0], "verse_count": r[1]} for r in cursor.fetchall()]

            # Count entity categories
            cursor.execute("SELECT entity_category, COUNT(*) FROM entities GROUP BY entity_category;")
            categories = [{"id": r[0], "label": r[0].capitalize(), "entity_count": r[1]} for r in cursor.fetchall()]

            # Count doc_types
            cursor.execute("SELECT doc_type, COUNT(*) FROM documents GROUP BY doc_type;")
            doc_types = [{"id": r[0], "label": r[0].capitalize() + "s", "count": r[1]} for r in cursor.fetchall()]

            cursor.execute("SELECT COUNT(*) FROM documents;")
            total_docs = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM entities;")
            total_entities = cursor.fetchone()[0]

            return {
                "works":             works,
                "entity_categories": categories,
                "doc_types":         doc_types,
                "total_documents":   total_docs,
                "total_entities":    total_entities,
                "corpus_version":    "2B-4"
            }

    def get_random_verse(self, work: str = "all", entity_id: str = None) -> Optional[Dict[str, Any]]:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            where_clauses = ["doc_type = 'verse'"]
            params = []
            if work != "all":
                where_clauses.append("source_work = ?")
                params.append(work)
            if entity_id:
                where_clauses.append("entity_ids LIKE ?")
                params.append(f'%"{entity_id}"%')

            where_sql = f"WHERE {' AND '.join(where_clauses)}"
            cursor.execute(f"SELECT document_id FROM documents {where_sql};", params)
            rows = cursor.fetchall()
            if not rows:
                return None
            selected_id = random.choice(rows)[0]
            
        return self.get_document_by_id(selected_id)


class PostgresDocumentRepository(BaseDocumentRepository):
    """
    Placeholder repository implementing production database access on PostgreSQL.
    Allows backend to switch databases by changing dependencies without modifying endpoints.
    """
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError("PostgreSQL repository is designed but not implemented in Phase 3A.")

    def search_lexical(self, q: str, doc_type: str = "all", work: str = "all",
                       author: str = "all", entity_id: str = None, category: str = None,
                       page: int = 1, per_page: int = 20, sort: str = "relevance") -> Tuple[List[Dict[str, Any]], int]:
        raise NotImplementedError("PostgreSQL repository is designed but not implemented in Phase 3A.")

    def search_vector(self, q: str, doc_type: str = "all", work: str = "all",
                      author: str = "all", entity_id: str = None, page: int = 1,
                      per_page: int = 20) -> Tuple[List[Dict[str, Any]], int]:
        raise NotImplementedError("PostgreSQL repository is designed but not implemented in Phase 3B.")

    def search_hybrid(self, q: str, doc_type: str = "all", work: str = "all",
                      author: str = "all", entity_id: str = None, page: int = 1,
                      per_page: int = 20) -> Tuple[List[Dict[str, Any]], int]:
        raise NotImplementedError("PostgreSQL repository is designed but not implemented in Phase 3B.")

    def get_entity_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError("PostgreSQL repository is designed but not implemented in Phase 3A.")

    def get_plant_by_id(self, plant_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError("PostgreSQL repository is designed but not implemented in Phase 3A.")

    def get_siddhar_by_id(self, siddhar_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError("PostgreSQL repository is designed but not implemented in Phase 3A.")

    def get_work_by_id(self, work_id: str, collection: str = "all", page: int = 1, per_page: int = 50) -> Optional[Dict[str, Any]]:
        raise NotImplementedError("PostgreSQL repository is designed but not implemented in Phase 3A.")

    def get_formulation_by_id(self, formulation_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError("PostgreSQL repository is designed but not implemented in Phase 3A.")

    def list_collections(self) -> Dict[str, Any]:
        raise NotImplementedError("PostgreSQL repository is designed but not implemented in Phase 3A.")

    def get_random_verse(self, work: str = "all", entity_id: str = None) -> Optional[Dict[str, Any]]:
        raise NotImplementedError("PostgreSQL repository is designed but not implemented in Phase 3A.")
