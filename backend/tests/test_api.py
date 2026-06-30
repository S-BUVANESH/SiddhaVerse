import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_api_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert json_data["data"]["database_connected"] is True


def test_api_search_success():
    response = client.get("/api/v1/search?q=Pranayama")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert "results" in json_data["data"]
    assert len(json_data["data"]["results"]) > 0
    assert "evidence_package" in json_data["meta"]


def test_api_search_greeting():
    response = client.get("/api/v1/search?q=Hello")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert "results" in json_data["data"]
    assert len(json_data["data"]["results"]) == 0
    assert "greeting" in json_data["meta"]["intent"]["category"]
    assert "message" in json_data["data"]


def test_api_search_out_of_scope():
    response = client.get("/api/v1/search?q=quantum+physics+mechanics")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert len(json_data["data"]["results"]) == 0
    assert json_data["meta"]["intent"]["category"] == "out_of_scope"
    assert "message" in json_data["data"]


def test_api_get_verse():
    response = client.get("/api/v1/verse/sivavakkiyar_pm_0609")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert json_data["data"]["document_id"] == "sivavakkiyar_pm_0609"
    assert "tamil_text" in json_data["data"]


def test_api_get_verse_not_found():
    response = client.get("/api/v1/verse/non_existent_verse_id_9999")
    assert response.status_code == 404


def test_api_get_entity():
    response = client.get("/api/v1/entity/deity_shiva?include_verses=true&include_crossrefs=true")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert json_data["data"]["entity_id"] == "deity_shiva"
    assert "sample_verse_ids" in json_data["data"]
    assert "co_occurring_entities" in json_data["data"]


def test_api_get_plant():
    response = client.get("/api/v1/plant/plant_tulsi")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert json_data["data"]["document_id"] == "plant_tulsi"
    assert "scientific_name" in json_data["data"]


def test_api_get_siddhar():
    response = client.get("/api/v1/siddhar/siddhar_thirumoolar")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert json_data["data"]["document_id"] == "siddhar_thirumoolar"
    assert "Thirumoolar" in json_data["data"]["name"]


def test_api_get_work():
    response = client.get("/api/v1/work/thirumandiram?page=1&per_page=10")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert json_data["data"]["work_id"] == "thirumandiram"
    assert len(json_data["data"]["verses"]) > 0


def test_api_get_formulation():
    response = client.get("/api/v1/formulation/formulation_kabasura_kudineer")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert json_data["data"]["document_id"] == "formulation_kabasura_kudineer"


def test_api_list_collections():
    response = client.get("/api/v1/collections")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert "works" in json_data["data"]
    assert "entity_categories" in json_data["data"]
