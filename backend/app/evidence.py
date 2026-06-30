from typing import List, Dict, Any
from backend.app.config import settings

class EvidenceBuilder:
    def __init__(self, max_tokens: int = None):
        self.max_tokens = max_tokens or settings.max_context_tokens

    def _estimate_tokens(self, text: str) -> int:
        """Rough estimation of token count using word splits (1 token ≈ 0.75 words, so words / 0.75)."""
        if not text:
            return 0
        words = len(text.split())
        return int(words / 0.75)

    def build_evidence_package(self, raw_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Processes candidate records into a curated, LLM-ready Context Evidence Package.
        1. Deduplicates based on document_id.
        2. Sorts to prioritize primary verses (doc_type == "verse") over secondary docs.
        3. Enforces token budgets.
        """
        # 1. Deduplicate while preserving order of first appearance
        seen_ids = set()
        deduped = []
        for doc in raw_results:
            doc_id = doc.get("document_id")
            if not doc_id:
                continue
            if doc_id not in seen_ids:
                seen_ids.add(doc_id)
                deduped.append(doc)

        # 2. Separate primary and secondary sources
        primary_sources = []
        secondary_sources = []
        for doc in deduped:
            if doc.get("doc_type") == "verse":
                primary_sources.append(doc)
            else:
                secondary_sources.append(doc)

        # Re-merge: primary sources rank first, followed by secondary sources
        sorted_docs = primary_sources + secondary_sources

        # 3. Build context packages and respect token budgets
        selected_docs = []
        current_tokens = 0
        
        # Structure format tokens overhead is budgeted at 50 tokens per document
        OVERHEAD_TOKENS = 50

        for doc in sorted_docs:
            content_parts = [
                doc.get("tamil_text") or "",
                doc.get("transliteration") or "",
                doc.get("english_translation") or "",
                doc.get("search_text") or "",
                doc.get("biography") or "",
                doc.get("uses") or "",
                doc.get("indications") or "",
                doc.get("subject") or "",
                doc.get("preparation") or ""
            ]
            content_str = " ".join(part for part in content_parts if part)
            doc_tokens = self._estimate_tokens(content_str) + OVERHEAD_TOKENS
            
            if current_tokens + doc_tokens <= self.max_tokens:
                selected_docs.append(doc)
                current_tokens += doc_tokens
            else:
                # If we exceed token budget, stop adding. Primary sources are preserved.
                break

        # 4. Generate context formatting string
        context_str_parts = ["[START CONTEXT]"]
        for doc in selected_docs:
            doc_id = doc.get("document_id")
            val_hash = doc.get("content_hash") or "unknown_hash"
            work = doc.get("source_work") or "SiddhaVerse"
            num = doc.get("verse_number") or ""
            author = doc.get("author") or "Unknown"
            doc_type = doc.get("doc_type") or "other"

            meta_header = f"---\nSource ID: {doc_id}\nSource Hash: {val_hash}\nSource Work: {work}"
            if num:
                meta_header += f"\nVerse Number: {num}"
            meta_header += f"\nAuthor: {author}\nCategory: {doc_type}\nContent:"
            
            # Extract content text depending on doc_type
            if doc_type == "verse":
                body = doc.get("tamil_text") or ""
                trans = doc.get("transliteration") or ""
                body_block = f"{body}\n(Transliteration: {trans})"
            else:
                # For non-verse metadata, join core descriptive fields
                desc_parts = []
                for field in ["description", "biography", "uses", "indications", "subject", "preparation"]:
                    if doc.get(field):
                        desc_parts.append(f"{field.capitalize()}: {doc[field]}")
                if doc.get("scientific_name"):
                    desc_parts.insert(0, f"Scientific Name: {doc['scientific_name']}")
                body_block = "\n".join(desc_parts) if desc_parts else (doc.get("search_text") or "")

            context_str_parts.append(f"{meta_header}\n{body_block}")

        context_str_parts.append("---\n[END CONTEXT]")
        final_context_package = "\n".join(context_str_parts)

        return {
            "context_package": final_context_package,
            "documents": selected_docs,
            "total_tokens_estimated": current_tokens,
            "document_count": len(selected_docs)
        }
