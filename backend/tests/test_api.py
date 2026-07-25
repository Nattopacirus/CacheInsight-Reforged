from fastapi.testclient import TestClient
from main import app
import json
import time

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_simulate_endpoint():
    config = {
        "cache_size": 1,
        "block_size": 16,
        "mapping_type": "Direct"
    }
    file_content = b"Address\n0000\n0010\n0020\n0000"
    
    response = client.post(
        "/api/simulate",
        data={"config": json.dumps(config)},
        files={"file": ("test.csv", file_content, "text/csv")}
    )
    
    assert response.status_code == 202
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "Pending"
    
    # Optional: wait a moment for the process pool to finish if we want to ensure it doesn't crash
    time.sleep(1)
