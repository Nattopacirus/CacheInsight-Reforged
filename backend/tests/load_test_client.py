import time
import requests
import json
import sys

def run_load_test():
    url = "http://127.0.0.1:8000/api/simulate"
    filepath = "1M_addresses.csv"
    
    config = {
        "cache_size": 32,
        "block_size": 64,
        "mapping_type": "Direct",
        "replacement_policy": "LRU"
    }

    print("Uploading 1M_addresses.csv to start simulation...")
    start_time = time.time()
    try:
        with open(filepath, 'rb') as f:
            files = {'file': ('1M_addresses.csv', f, 'text/csv')}
            data = {'config': json.dumps(config)}
            response = requests.post(url, files=files, data=data, timeout=30)
            response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("ERROR: API Server is not running. Please start the backend on port 8000.")
        return
    except Exception as e:
        print(f"Failed to start simulation: {e}")
        return

    job_id = response.json().get("job_id")
    print(f"Job started with ID: {job_id}")

    # Poll status
    status_url = f"http://127.0.0.1:8000/api/simulate/{job_id}"
    while True:
        try:
            res = requests.get(status_url, timeout=10)
            res.raise_for_status()
            job = res.json()
            
            print(f"Status: {job['status']} | Progress: {job['progress']}%")
            
            if job['status'] in ['Completed', 'Failed']:
                end_time = time.time()
                print(f"Finished in {end_time - start_time:.2f} seconds.")
                if job['status'] == 'Completed':
                    print("Result:")
                    print(json.dumps(job['result'], indent=2))
                else:
                    print(f"Error: {job.get('result')}")
                break
                
            time.sleep(1)
        except Exception as e:
            print(f"Polling failed: {e}")
            break

if __name__ == "__main__":
    run_load_test()
