import os
import re
import logging
import requests
from typing import List, Dict, Any, Optional

logger = logging.getLogger("siddhaverse_api.llm")

class LLMEngine:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.model_name = os.environ.get("GEMINI_MODEL", "gemini-1.5-pro")
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"

    def generate(self, prompt: str, context_docs: List[Dict[str, Any]], query: str) -> str:
        """Generates response using Gemini API if configured, otherwise falls back to local simulation."""
        if self.api_key:
            try:
                logger.info(f"Invoking real Gemini API using model {self.model_name}")
                headers = {"Content-Type": "application/json"}
                params = {"key": self.api_key}
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.0,
                        "maxOutputTokens": 1024
                    }
                }
                response = requests.post(self.api_url, json=payload, headers=headers, params=params, timeout=15)
                response.raise_for_status()
                data = response.json()
                if "candidates" in data and len(data["candidates"]) > 0:
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    return text.strip()
                raise ValueError("No candidates returned from Gemini API")
            except Exception as e:
                logger.error(f"Gemini API invocation failed: {e}. Falling back to local simulator.")
        
        return self._simulate_generation(context_docs, query)

    def _simulate_generation(self, context_docs: List[Dict[str, Any]], query: str) -> str:
        """Simulates a highly accurate, citation-constrained scholarly RAG response from context."""
        q_lower = query.lower()
        
        # Check greeting
        if any(g in q_lower for g in ["hello", "hi", "hey", "namaste", "vanakkam"]):
            return "Greetings! I am the SiddhaVerse Scholarly Retrieval Assistant. How can I help you explore the texts today?"

        # Check out of scope
        if not context_docs:
            return "The SiddhaVerse corpus does not contain evidence to answer this query."

        # Find the most relevant document based on exact text overlap or matching expected text
        target_doc = None
        for doc in context_docs:
            tamil = (doc.get("tamil_text") or "").lower()
            trans = (doc.get("transliteration") or "").lower()
            title = (doc.get("title") or "").lower()
            desc = (doc.get("description") or "").lower()
            search = (doc.get("search_text") or "").lower()
            
            # Simple matching logic
            words = [w for w in re.split(r'\W+', q_lower) if len(w) > 3]
            match_count = sum(1 for w in words if w in tamil or w in trans or w in title or w in desc or w in search)
            
            if match_count > 0 or not words:
                target_doc = doc
                break
        
        if not target_doc:
            target_doc = context_docs[0]

        doc_id = target_doc.get("document_id")
        val_hash = target_doc.get("content_hash") or "unknown_hash"
        work = target_doc.get("source_work") or "SiddhaVerse"
        num = target_doc.get("verse_number") or ""
        doc_type = target_doc.get("doc_type") or "other"

        # Generate a structured answer strictly backed by target_doc
        if doc_type == "verse":
            tamil_text = target_doc.get("tamil_text") or ""
            trans = target_doc.get("transliteration") or ""
            eng_trans = target_doc.get("english_translation") or ""
            
            snippet = eng_trans if eng_trans else (trans if trans else tamil_text)
            # Remove linebreaks for the inline statement
            snippet = snippet.replace("\n", " ").strip()
            
            ans = f"According to {work} verse {num}, the text states: '{snippet}'. <cite doc=\"{doc_id}\" hash=\"{val_hash}\" />"
        elif doc_type == "plant":
            title = target_doc.get("title") or "The plant"
            scientific = target_doc.get("scientific_name") or ""
            uses = target_doc.get("uses") or target_doc.get("description") or ""
            scientific_str = f" ({scientific})" if scientific else ""
            
            ans = f"In Siddha medicine, {title}{scientific_str} is documented for its therapeutic properties: {uses}. <cite doc=\"{doc_id}\" hash=\"{val_hash}\" />"
        elif doc_type == "formulation":
            title = target_doc.get("title") or "The formulation"
            prep = target_doc.get("preparation") or target_doc.get("description") or ""
            
            ans = f"The traditional formulation {title} is prepared and indicated as follows: {prep}. <cite doc=\"{doc_id}\" hash=\"{val_hash}\" />"
        elif doc_type == "biography":
            title = target_doc.get("title") or "The Siddhar"
            bio = target_doc.get("biography") or target_doc.get("description") or ""
            
            ans = f"Siddhar {title} is a prominent figure in the Siddha tradition: {bio}. <cite doc=\"{doc_id}\" hash=\"{val_hash}\" />"
        else:
            desc = target_doc.get("description") or target_doc.get("search_text") or "details available in corpus"
            ans = f"Siddha document {doc_id} outlines: {desc}. <cite doc=\"{doc_id}\" hash=\"{val_hash}\" />"

        return ans
