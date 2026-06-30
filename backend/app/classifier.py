import re
from typing import Dict, Any

class QueryClassifier:
    def __init__(self):
        # 1. Compile regex patterns for fast classification matching
        self.patterns = {
            "greeting": re.compile(
                r"\b(hello|hi|hey|greetings|good\s+morning|good\s+afternoon|good\s+evening|namaste|vanakkam)\b", 
                re.IGNORECASE
            ),
            "verse_lookup": re.compile(
                r"\b(verse|song|poem|padal|padalgal|thirumandiram|sivavakkiyam|tantiram)\s*[-_:#]?\s*(\d+)\b|\b(verse|song|padal)\s+(\d+)\b",
                re.IGNORECASE
            ),
            "siddhar_biography": re.compile(
                r"\b(thirumoolar|sivavakkiyar|agasthiyar|bogar|nandidevar|karuvoorar|machamuni|konkanar|pambatti|ramadevar|korakkar|kudambai|idaikkadar|theriyar|sattaimuni|yugi|siddhar|siddhars|sage|saint)\b",
                re.IGNORECASE
            ),
            "medicinal_plant": re.compile(
                r"\b(plant|herb|basil|tulsi|lotus|thamarai|thippili|pepper|ginger|inji|sukku|nelli|amla|manjal|turmeric|milagu|ashwagandha|kadukkai|keezhanelli|keelanelli|neem|vembu|adathodai|nilavembu|musumusukkai|vilvam|seenthil|omam|karpuram|camphor|thandrikai|kanchanaram)\b",
                re.IGNORECASE
            ),
            "formulation": re.compile(
                r"\b(formulation|recipe|medicine|chooranam|choornam|kudineer|decoction|thailam|oil|ney|ghritham|parpam|parpam|kuzhambu|guligai|ney|rasayanam|lehyam|bhasma|churna)\b",
                re.IGNORECASE
            ),
            "sacred_place": re.compile(
                r"\b(place|temple|hill|mountain|chidambaram|thillai|tiruvannamalai|arunachala|kailash|kailasa|kashi|varanasi|madurai|potigai|himalaya|himalayas)\b",
                re.IGNORECASE
            ),
            "research_article": re.compile(
                r"\b(pubmed|pmc|pmid|study|studies|trial|trials|clinical|research|paper|papers|journal|article|articles|scientific|efficacy|in\s+vitro|in\s+vivo|activity)\b",
                re.IGNORECASE
            )
        }

        # Whitelist of valid topics for out-of-scope filter
        self.valid_topics = [
            "siddha", "medicine", "herb", "plant", "verse", "song", "poem", "padal", 
            "tantiram", "thirumandiram", "sivavakkiyam", "siddhar", "yogi", "spirit",
            "yoga", "meditation", "pranayama", "breath", "kumbhaka", "shiva", "shakti",
            "deity", "philosophy", "chakra", "kundalini", "alchemy", "rejuvenation",
            "kayakalpa", "varma", "health", "remedy", "disease", "treatment", "cure",
            "manuscript", "palm leaf", "catalog", "library", "pmid", "pubmed", "science",
            "recipe", "decoction", "kudineer", "chooranam", "formulation", "kabasura"
        ]

    def classify(self, query: str) -> Dict[str, Any]:
        """
        Classify the query intent.
        Returns a dict: {"category": str, "confidence": float, "details": dict}
        """
        q = query.strip()
        if not q:
            return {"category": "out_of_scope", "confidence": 1.0, "reason": "Empty query"}

        # 1. Check Greetings
        if self.patterns["greeting"].search(q):
            return {"category": "greeting", "confidence": 1.0, "reason": "Matches conversational patterns"}

        # 2. Out-of-Scope Pre-check: Verify query contains at least one relevant concept
        words = re.findall(r"\b\w+\b", q.lower())
        # If query is long and has no keywords in whitelist, mark out_of_scope
        if len(words) >= 3:
            has_relevant_word = False
            for w in words:
                if any(topic in w for topic in self.valid_topics):
                    has_relevant_word = True
                    break
            if not has_relevant_word:
                # Also check if it's in Tamil script (Tamil character range is \u0b80-\u0bff)
                is_tamil = any("\u0b80" <= char <= "\u0bff" for char in q)
                if not is_tamil:
                    return {
                        "category": "out_of_scope", 
                        "confidence": 0.9, 
                        "reason": "Query does not relate to Siddha, plants, medicine, or philosophy."
                    }

        # 3. Check Verse Lookup
        verse_match = self.patterns["verse_lookup"].search(q)
        if verse_match:
            groups = verse_match.groups()
            verse_num = next((g for g in groups if g and g.isdigit()), None)
            return {
                "category": "verse_lookup",
                "confidence": 0.95,
                "details": {"verse_number": verse_num}
            }

        # 4. Check Research Articles
        if self.patterns["research_article"].search(q):
            return {"category": "research_article", "confidence": 0.85}

        # 5. Check Formulations
        if self.patterns["formulation"].search(q):
            return {"category": "formulation", "confidence": 0.85}

        # 6. Check Medicinal Plants
        if self.patterns["medicinal_plant"].search(q):
            return {"category": "medicinal_plant", "confidence": 0.85}

        # 7. Check Sacred Places
        if self.patterns["sacred_place"].search(q):
            return {"category": "sacred_place", "confidence": 0.85}

        # 8. Check Siddhar Biographies
        if self.patterns["siddhar_biography"].search(q):
            return {"category": "siddhar_biography", "confidence": 0.85}

        # 9. Fallback to general philosophy search (requires hybrid retrieval)
        return {"category": "philosophy", "confidence": 0.6}
