import requests
import time
import csv
import concurrent.futures

# AWS Lambda endpoint (for commercial)
ENDPOINT = "https://6onxqkpo90.execute-api.eu-north-1.amazonaws.com/default/ml"

# Payload: base64 1x1 image (purple)
PAYLOAD = {
    "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNcItVfDwAEhQHOtf/DfQAAAABJRU5ErkJggg=="
}

HEADERS = {'Content-Type': 'application/json'}

# Number of requests to send
TOTAL_REQUESTS = 200
CONCURRENCY = 10
CSV_FILENAME = "lambda_benchmark_results.csv"


def send_request(i):
    try:
        start_time = time.time()
        response = requests.post(ENDPOINT, json=PAYLOAD, headers=HEADERS)
        end_time = time.time()
        duration = round((end_time - start_time) * 1000, 2)  # in ms

        data = response.json()
        status = response.status_code
        start_type = data.get('start_type', 'unknown')

        return {
            "request_id": i + 1,
            "status_code": status,
            "duration_ms": duration,
            "start_type": start_type
        }
    except Exception as e:
        return {
            "request_id": i + 1,
            "status_code": 0,
            "duration_ms": 0,
            "start_type": "error",
            "error": str(e)
        }


def run_benchmark():
    results = []
    print(f"Starting benchmark with {TOTAL_REQUESTS} requests (concurrency: {CONCURRENCY})...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = [executor.submit(send_request, i) for i in range(TOTAL_REQUESTS)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"[#{result['request_id']}] Status: {result['status_code']}, Time: {result['duration_ms']}ms, Start: {result['start_type']}")

    # Save results to CSV
    with open(CSV_FILENAME, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\n Benchmark complete. Results saved to: {CSV_FILENAME}")


if __name__ == "__main__":
    run_benchmark()
