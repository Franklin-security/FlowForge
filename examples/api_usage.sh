#!/bin/bash

# FlowForge API Usage Examples
# These examples demonstrate how to use FlowForge via REST API

BASE_URL="http://localhost:8000"

echo "=========================================="
echo "FlowForge API Usage Examples"
echo "=========================================="
echo ""

# Health check
echo "1. Health Check:"
curl -s "$BASE_URL/health" | jq .
echo ""
echo ""

# Application info
echo "2. Application Info:"
curl -s "$BASE_URL/api/v1/info" | jq .
echo ""
echo ""

# Add a provider
echo "3. Add GitHub Provider:"
curl -s -X POST "$BASE_URL/api/v1/providers" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "github-main",
    "type": "github",
    "token": "your_token_here",
    "owner": "your-org",
    "repo": "your-repo",
    "enabled": true,
    "refresh_interval": 30
  }' | jq .
echo ""
echo ""

# List providers
echo "4. List Providers:"
curl -s "$BASE_URL/api/v1/providers" | jq .
echo ""
echo ""

# List pipelines
echo "5. List All Pipelines:"
curl -s "$BASE_URL/api/v1/pipelines" | jq .
echo ""
echo ""

# List pipelines from specific provider
echo "6. List Pipelines from Provider:"
curl -s "$BASE_URL/api/v1/pipelines/github-main/pipelines" | jq .
echo ""
echo ""

# Trigger a pipeline
echo "7. Trigger Pipeline:"
curl -s -X POST "$BASE_URL/api/v1/pipelines/github-main/pipelines/WORKFLOW_ID/trigger" \
  -H "Content-Type: application/json" \
  -d '{
    "ref": "main",
    "inputs": {
      "environment": "production"
    }
  }' | jq .
echo ""
echo ""

# Cancel a run
echo "8. Cancel Pipeline Run:"
curl -s -X POST "$BASE_URL/api/v1/pipelines/github-main/runs/RUN_ID/cancel" | jq .
echo ""
echo ""

echo "=========================================="
echo "Examples complete!"
echo "=========================================="

