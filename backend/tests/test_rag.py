import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.rag import CitationVerifier, RAGPipeline
from backend.app.repositories import SQLiteDocumentRepository

client = TestClient(app)

def test_rag_greeting():
    response = client.get("/api/v1/rag?q=hello")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert "Greetings" in json_data["data"]["answer"]
    assert len(json_data["data"]["citations"]) == 0

def test_rag_out_of_scope():
    response = client.post("/api/v1/rag", json={"query": "Explain quantum physics"})
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert "falls outside the scope" in json_data["data"]["answer"]
    assert len(json_data["data"]["citations"]) == 0

def test_rag_unsupported_query():
    # A query in Tamil script (bypassing out_of_scope regex) but has zero matches in database
    response = client.get("/api/v1/rag?q=இல்லாதவார்த்தைசும்மா")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert "does not contain evidence" in json_data["data"]["answer"]
    assert len(json_data["data"]["citations"]) == 0


def test_rag_valid_query():
    # Use a query with "நினைப்பதொன்று" that will match sivavakkiyar_pm_0616 or similar
    response = client.get("/api/v1/rag?q=நினைப்பதொன்று கண்டிலேன்")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert len(json_data["data"]["citations"]) > 0
    citation = json_data["data"]["citations"][0]
    assert "document_id" in citation
    assert "source_work" in citation
    assert "hash" not in citation  # Hash is removed from final client response as it is an internal security check

def test_citation_verifier_success():
    injected = [
        {"document_id": "doc1", "content_hash": "hash1", "source_work": "Work A", "verse_number": "1", "source_url": None}
    ]
    output = "Facts match. <cite doc=\"doc1\" hash=\"hash1\" />"
    valid, msg, citations = CitationVerifier.verify(output, injected)
    assert valid is True
    assert msg == "Success"
    assert len(citations) == 1
    assert citations[0]["document_id"] == "doc1"
    assert citations[0]["source_work"] == "Work A"

def test_citation_verifier_hallucinated_doc():
    injected = [
        {"document_id": "doc1", "content_hash": "hash1", "source_work": "Work A", "verse_number": "1", "source_url": None}
    ]
    output = "Facts match. <cite doc=\"fake_doc\" hash=\"hash1\" />"
    valid, msg, citations = CitationVerifier.verify(output, injected)
    assert valid is False
    assert "Hallucinated document" in msg
    assert len(citations) == 0

def test_citation_verifier_mismatched_hash():
    injected = [
        {"document_id": "doc1", "content_hash": "hash1", "source_work": "Work A", "verse_number": "1", "source_url": None}
    ]
    output = "Facts match. <cite doc=\"doc1\" hash=\"wrong_hash\" />"
    valid, msg, citations = CitationVerifier.verify(output, injected)
    assert valid is False
    assert "Mismatched content hash" in msg
    assert len(citations) == 0
