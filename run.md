curl -s -X POST http://localhost:5001/api/graph/ontology/generate \
  -F "files=@test/seed.md" \
  -F "simulation_requirement=Simulate a policy debate about Ethiopia digital payment competition between Telebirr and M-Pesa" \
  -F "project_name=Test Ethiopia" 2>&1 | head -50


  Error code: 413 - Limit 8000, Requested 14250
