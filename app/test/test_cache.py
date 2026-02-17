import httpx
import time
import json

# Configuration - Change this to your local server URL
BASE_URL = "http://127.0.0.1:8000/api/v1/certificate"
# Use a code that exists in your database
VERIFY_CODE = "KSHRD-TEST-CODE-20266" 

def test_caching_performance():
    print(f"--- Testing Cache for Code: {VERIFY_CODE} ---")

    # 1. First Request: Expecting a Cache MISS (Hitting DB + Keycloak)
    start_time = time.perf_counter()
    response1 = httpx.get(f"{BASE_URL}/{VERIFY_CODE}/verify")
    end_time = time.perf_counter()
    
    first_duration = (end_time - start_time) * 1000 # convert to ms
    print(f"Request 1 (MISS/DB): {first_duration:.2f} ms")
    assert response1.status_code == 200

    # 2. Second Request: Expecting a Cache HIT (Hitting Redis)
    start_time = time.perf_counter()
    response2 = httpx.get(f"{BASE_URL}/{VERIFY_CODE}/verify")
    end_time = time.perf_counter()
    
    second_duration = (end_time - start_time) * 1000 # convert to ms
    print(f"Request 2 (HIT/Redis): {second_duration:.2f} ms")
    assert response2.status_code == 200

    # 3. Analysis
    improvement = ((first_duration - second_duration) / first_duration) * 100
    print(f"Speed Improvement: {improvement:.2f}%")
    
    if second_duration < first_duration * 0.5:
        print("✅ SUCCESS: The second request was significantly faster. Redis is working!")
    else:
        print("⚠️ WARNING: The second request time is similar. Check if caching logic is active.")

if __name__ == "__main__":
    test_caching_performance()