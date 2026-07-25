import os
import json
import concurrent.futures
from models import SimulationJob
from database import SessionLocal
from app.simulator.core import direct_map, fully_associative, set_associative

executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)

def _process_in_worker(job_id: str, file_path: str, config: dict):
    # This runs in a separate process, so we create our own DB session
    db = SessionLocal()
    try:
        # 1. Update status to Processing
        job = db.query(SimulationJob).filter(SimulationJob.id == job_id).first()
        if not job:
            return
        job.status = "Processing"
        db.commit()

        # 2. Read addresses from CSV (skip header)
        addresses = []
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) > 0:
                # assuming first line is header
                lines = lines[1:]
            for line in lines:
                addr = line.strip()
                if addr:
                    if addr.lower().startswith('0x'):
                        addr = addr[2:]
                    addresses.append(addr)

        total_lines = len(addresses)
        
        # 3. Define progress callback
        def progress_callback(processed: int, total: int):
            job = db.query(SimulationJob).filter(SimulationJob.id == job_id).first()
            if job:
                job.progress = int((processed / total) * 100)
                db.commit()

        # 4. Run simulation
        mapping_type = config.get("mapping_type", "Direct")
        cache_size_kb = int(config.get("cache_size", 1))
        block_size = int(config.get("block_size", 16))
        
        if mapping_type == "Direct":
            result = direct_map(cache_size_kb, block_size, addresses, progress_callback)
        elif mapping_type == "Fully":
            result = fully_associative(cache_size_kb, block_size, addresses, progress_callback)
        elif mapping_type == "Set":
            sets = int(config.get("n_way", 2))
            result = set_associative(cache_size_kb, block_size, sets, addresses, progress_callback)
        else:
            raise ValueError(f"Unknown mapping type: {mapping_type}")

        # 5. Save result and mark as Completed
        result["total_accesses"] = result.get("hits", 0) + result.get("misses", 0)
        result["config"] = config
        
        job = db.query(SimulationJob).filter(SimulationJob.id == job_id).first()
        if job:
            job.status = "Completed"
            job.progress = 100
            job.result = json.dumps(result)
            db.commit()

    except Exception as e:
        job = db.query(SimulationJob).filter(SimulationJob.id == job_id).first()
        if job:
            job.status = "Failed"
            job.result = str(e)
            db.commit()
    finally:
        db.close()
        # Clean up file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

def run_simulation_job(job_id: str, file_path: str, config: dict):
    # Submit the task to the ProcessPoolExecutor to avoid blocking the event loop
    executor.submit(_process_in_worker, job_id, file_path, config)
