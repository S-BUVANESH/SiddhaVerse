import re
import logging
from typing import List, Dict, Any, Tuple, Optional

from backend.app.classifier import QueryClassifier
from backend.app.evidence import EvidenceBuilder
from backend.app.llm import LLMEngine
from backend.app.repositories import BaseDocumentRepository

logger = logging.getLogger("siddhaverse_api.rag")

class CitationVerifier:
    @staticmethod
    def verify(llm_output: str, injected_docs: List[Dict[str, Any]]) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """
        Parses and validates citations inside the LLM response.
        Returns:
            Tuple[is_valid, status_message, list_of_verified_citation_dicts]
        """
        # Build map of injected document_id -> content_hash & metadata
        doc_map = {}
        for doc in injected_docs:
            doc_id = doc.get("document_id")
            if doc_id:
                doc_map[doc_id] = {
                    "hash": doc.get("content_hash") or "unknown_hash",
                    "source_work": doc.get("source_work") or "SiddhaVerse",
                    "verse_number": doc.get("verse_number"),
                    "source_url": doc.get("source_url")
                }

        # Find all <cite doc="..." hash="..." /> tags
        # Allowing some whitespace or minor variations in casing
        citations = re.findall(r'<cite\s+doc="([^"]+)"\s+hash="([^"]+)"\s*/>', llm_output)
        
        verified_citations = []
        seen_ids = set()

        for doc_id, val_hash in citations:
            if doc_id not in doc_map:
                logger.warning(f"Hallucinated document ID detected: '{doc_id}'")
                return False, "Security Error: Hallucinated document citation detected.", []
            
            expected_hash = doc_map[doc_id]["hash"]
            if expected_hash != val_hash:
                logger.warning(f"Mismatched content hash for '{doc_id}': expected '{expected_hash}', got '{val_hash}'")
                return False, "Security Error: Mismatched content hash detected.", []

            if doc_id not in seen_ids:
                seen_ids.add(doc_id)
                citation_meta = {
                    "document_id": doc_id,
                    "source_work": doc_map[doc_id]["source_work"],
                    "source_url": doc_map[doc_id]["source_url"]
                }
                if doc_map[doc_id]["verse_number"]:
                    citation_meta["verse_number"] = doc_map[doc_id]["verse_number"]
                verified_citations.append(citation_meta)

        return True, "Success", verified_citations


class RAGPipeline:
    def __init__(self, repo: BaseDocumentRepository):
        self.repo = repo
        self.classifier = QueryClassifier()
        self.evidence_builder = EvidenceBuilder()
        self.llm = LLMEngine()

    def run(self, query: str) -> Dict[str, Any]:
        """Runs the complete citation-constrained RAG pipeline."""
        query_str = query.strip()
        if not query_str:
            return {
                "answer": "The SiddhaVerse corpus does not contain evidence to answer this query.",
                "citations": [],
                "meta": {"intent": {"category": "out_of_scope", "confidence": 1.0}}
            }

        # 1. Classify Intent
        intent = self.classifier.classify(query_str)
        category_intent = intent.get("category")

        # 2. Greeting / Out-of-Scope Pre-refusals
        if category_intent == "out_of_scope":
            return {
                "answer": "The query falls outside the scope of the SiddhaVerse library.",
                "citations": [],
                "meta": {"intent": intent}
            }

        if category_intent == "greeting":
            return {
                "answer": "Greetings! I am the SiddhaVerse Scholarly Retrieval Assistant. How can I help you explore the texts today?",
                "citations": [],
                "meta": {"intent": intent}
            }

        # 3. Hybrid Retrieval
        # Check if the query is a complete mismatch (nonsense / OOD)
        lex_hits, _ = self.repo.search_lexical(q=query_str, page=1, per_page=1)
        vec_hits, _ = self.repo.search_vector(q=query_str, page=1, per_page=1)
        
        if not lex_hits:
            if not vec_hits or vec_hits[0].get("score", 0.0) < 0.82:
                logger.info(f"Graceful refusal for mismatch query: '{query_str}' (Lexical: 0, Vector score: {vec_hits[0].get('score', 0.0) if vec_hits else 0.0})")
                return {
                    "answer": "The SiddhaVerse corpus does not contain evidence to answer this query.",
                    "citations": [],
                    "meta": {"intent": intent, "unsupported_reason": "No lexical match and low vector confidence"}
                }

        # We retrieve up to 10 candidates to ensure context fitting
        results, total = self.repo.search_hybrid(
            q=query_str, doc_type="all", work="all", author="all",
            page=1, per_page=10
        )

        # Filter results by strict confidence threshold (score >= 0.55) to prune semantic noise
        high_confidence_results = [doc for doc in results if doc.get("score", 0.0) >= 0.55]

        # 4. Context compilation
        evidence_pkg = self.evidence_builder.build_evidence_package(high_confidence_results)
        formatted_context = evidence_pkg["context_package"]
        injected_docs = evidence_pkg["documents"]

        # Graceful refusal if no evidence is found or if matching documents are empty
        if not injected_docs:
            return {
                "answer": "The SiddhaVerse corpus does not contain evidence to answer this query.",
                "citations": [],
                "meta": {
                    "intent": intent,
                    "retrieved_count": 0,
                    "total_tokens_estimated": 0
                }
            }

        # 5. Prompt Assembly
        prompt = f"""You are the SiddhaVerse AI Scholarly Assistant, a factual repository search assistant.
Your goal is to answer the user's query using ONLY the verified context documents provided below.

=== STRICT RULES ===
1. Answer the query using ONLY the facts explicitly mentioned in the [CONTEXT] block.
2. Do not use any external historical, religious, or medical knowledge.
3. If the context does not contain sufficient information to answer the query, state: "The SiddhaVerse corpus does not contain evidence to answer this query."
4. Every fact you state must be cited inline using the format: <cite doc="document_id" hash="content_hash" />. Place the tag immediately after the sentence containing the cited fact.
5. Do not write a summary bibliography at the end; place citations inline.

=== CONTEXT ===
{formatted_context}

=== USER QUERY ===
{query_str}

=== VERIFIED RESPONSE ===
"""

        # 6. LLM Inference
        raw_output = self.llm.generate(prompt, injected_docs, query_str)

        # 7. Post-Gen Citation Verification
        is_valid, msg, citations_meta = CitationVerifier.verify(raw_output, injected_docs)

        if not is_valid:
            return {
                "answer": "The assistant generated an unverified response. Result blocked for scholarly integrity.",
                "citations": [],
                "meta": {
                    "intent": intent,
                    "verification_error": msg,
                    "retrieved_count": len(injected_docs),
                    "total_tokens_estimated": evidence_pkg["total_tokens_estimated"]
                }
            }

        return {
            "answer": raw_output,
            "citations": citations_meta,
            "meta": {
                "intent": intent,
                "retrieved_count": len(injected_docs),
                "total_tokens_estimated": evidence_pkg["total_tokens_estimated"]
            }
        }
