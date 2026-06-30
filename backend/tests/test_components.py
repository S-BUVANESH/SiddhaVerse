import os
import pytest
from backend.app.classifier import QueryClassifier
from backend.app.evidence import EvidenceBuilder
from backend.app.repositories import SQLiteDocumentRepository

def test_query_classifier():
    classifier = QueryClassifier()

    # Greetings
    res = classifier.classify("Hello, how are you?")
    assert res["category"] == "greeting"

    # Out-of-scope
    res = classifier.classify("What is the stock price of Apple?")
    assert res["category"] == "out_of_scope"

    # Verse lookup
    res = classifier.classify("Thirumandiram verse 127")
    assert res["category"] == "verse_lookup"
    assert res["details"]["verse_number"] == "127"

    # Plant lookup
    res = classifier.classify("What are the uses of Tulsi herb?")
    assert res["category"] == "medicinal_plant"

    # Formulation lookup
    res = classifier.classify("Recipe for Kabasura Kudineer decoction")
    assert res["category"] == "formulation"

    # Sacred place lookup
    res = classifier.classify("Verses from Tiruvannamalai temple")
    assert res["category"] == "sacred_place"

    # Research article lookup
    res = classifier.classify("PubMed trials on clinical efficacy of basil")
    assert res["category"] == "research_article"

    # Fallback to philosophy
    res = classifier.classify("What is the union of Shiva and Shakti?")
    assert res["category"] == "philosophy"


def test_evidence_builder():
    builder = EvidenceBuilder(max_tokens=300)

    # Mock documents list
    docs = [
        {
            "document_id": "text_thirumandiram_pm_0001",
            "tamil_text": "ஒன்றவன் தானே இரண்டவன்",
            "transliteration": "onravan tane",
            "source_work": "Thirumandiram",
            "verse_number": "1",
            "author": "Thirumoolar",
            "doc_type": "verse"
        },
        {
            "document_id": "text_thirumandiram_pm_0001", # Duplicate id
            "tamil_text": "ஒன்றவன் தானே இரண்டவன்",
            "transliteration": "onravan tane",
            "source_work": "Thirumandiram",
            "verse_number": "1",
            "author": "Thirumoolar",
            "doc_type": "verse"
        },
        {
            "document_id": "plant_tulsi",
            "description": "Holy basil adaptogen",
            "source_work": "Siddha Materia Medica",
            "author": "SiddhaVerse",
            "doc_type": "plant"
        }
    ]

    package = builder.build_evidence_package(docs)
    
    # Verify deduplication
    assert len(package["documents"]) == 2
    assert package["document_count"] == 2
    assert "siddhar_thirumoolar" not in package["context_package"]

    # Verify context formatting contains headers and delimiters
    assert "[START CONTEXT]" in package["context_package"]
    assert "Source ID: text_thirumandiram_pm_0001" in package["context_package"]
    assert "Source ID: plant_tulsi" in package["context_package"]
    assert "[END CONTEXT]" in package["context_package"]


def test_repository_getters():
    repo = SQLiteDocumentRepository()

    # Get random verse
    verse = repo.get_random_verse()
    assert verse is not None
    assert verse["doc_type"] == "verse"
    assert "document_id" in verse

    # Get specific verse with adjacency checks
    doc_id = "sivavakkiyar_pm_0610"
    doc = repo.get_document_by_id(doc_id)
    assert doc is not None
    assert doc["document_id"] == doc_id
    assert "adjacent" in doc
    assert doc["adjacent"]["previous"] == "sivavakkiyar_pm_0609"
    assert doc["adjacent"]["next"] == "sivavakkiyar_pm_0611"

    # Get Entity lookup
    ent = repo.get_entity_by_id("deity_shiva")
    assert ent is not None
    assert ent["entity_name"] == "Shiva"
    assert ent["entity_category"] == "deities"
    assert ent["occurrence_count"] > 0

    # Get Plant lookup
    plant = repo.get_plant_by_id("plant_tulsi")
    assert plant is not None
    assert plant["scientific_name"] == "Ocimum sanctum"

    # Get Siddhar lookup
    siddhar = repo.get_siddhar_by_id("siddhar_thirumoolar")
    assert siddhar is not None
    assert "Thirumoolar" in siddhar["name"]

    # Get Formulation lookup
    form = repo.get_formulation_by_id("formulation_kabasura_kudineer")
    assert form is not None
    assert "Kabasura Kudineer" in form["title"]
