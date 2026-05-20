
docker compose up --build

curl [localhost](http://localhost:8000/health)

curl -X POST [localhost](http://localhost:8000/analyze) \
  -H "Content-Type: application/json" \
  -d '{
    "incident_id": "INC-1001",
    "query": "Analyze the incident and identify probable root cause"
  }'
