from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_query():
    response = client.post("/query", json={"question": "How many students are in the school?"})
    assert response.status_code == 200
    assert "answer" in response.json()