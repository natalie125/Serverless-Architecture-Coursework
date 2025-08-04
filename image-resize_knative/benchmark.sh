#!/bin/bash

ENDPOINT="http://resize-image.default.svc.cluster.local"
PAYLOAD='{"image":"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNcItVfDwAEhQHOtf/DfQAAAABJRU5ErkJggg=="}'

TOTAL_REQUESTS=200
CONCURRENCY=50
OUTPUT_FILE="benchmark_results.txt"

echo "Starting benchmark: $TOTAL_REQUESTS requests with concurrency $CONCURRENCY"
printf "%-6s | %-8s | %-10s\n" "ID" "Time" "Start" | tee "$OUTPUT_FILE"

i=1
while [ $i -le $TOTAL_REQUESTS ]; do
  for ((j=0; j<$CONCURRENCY && i+j<=TOTAL_REQUESTS; j++)); do
    (
      start=$(date +%s%3N)
      response=$(curl -s -X POST "$ENDPOINT" -H "Content-Type: application/json" -d "$PAYLOAD")
      end=$(date +%s%3N)
      duration=$((end - start))

      if echo "$response" | grep -q '"start_type"'; then
        start_type=$(echo "$response" | grep -o '"start_type":"[^"]*"' | cut -d':' -f2 | tr -d '"')
      else
        start_type="(none)"
      fi

      line=$(printf "[#%-3s] | %-6sms | %-10s" "$((i + j))" "$duration" "$start_type")
      echo "$line" | tee -a "$OUTPUT_FILE"
    ) &
  done
  wait
  i=$((i + CONCURRENCY))
done

echo -e "\nBenchmark complete!" | tee -a "$OUTPUT_FILE"