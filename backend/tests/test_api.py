from fastapi.testclient import TestClient
from main import app
import json
import time
import uuid
from database import SessionLocal
from models import SimulationJob

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

def test_get_simulation_status_not_found():
    response = client.get("/api/simulate/non-existent-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"

def test_get_simulation_status_found():
    # Insert a dummy job
    db = SessionLocal()
    dummy_job_id = str(uuid.uuid4())
    job = SimulationJob(
        id=dummy_job_id,
        status="Completed",
        progress=100,
        result=json.dumps({"hits": 100, "misses": 50, "hit_rate": 66.6, "miss_rate": 33.3})
    )
    db.add(job)
    db.commit()
    
    try:
        response = client.get(f"/api/simulate/{dummy_job_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["job_id"] == dummy_job_id
        assert data["status"] == "Completed"
        assert data["progress"] == 100
        assert data["result"]["hits"] == 100
    finally:
        # Cleanup
        db.delete(job)
        db.commit()
        db.close()
