#!/bin/bash

# Quick test script for Fraud Detection API

echo "=========================================="
echo "  Fraud Detection Service - API Tests"
echo "=========================================="

echo -e "\n1. Health Check:"
curl -s http://localhost:8000/health | python3 -m json.tool

echo -e "\n2. Low Risk Visit:"
curl -s -X POST "http://localhost:8000/evaluate-risk" \
  -H "Content-Type: application/json" \
  -d '{
    "visit_id": "VIS-TEST-001",
    "appointment_id": "APT-001",
    "national_id_hash": "ID-123456",
    "branch_id": "BR-001",
    "gate_id": "GATE-01",
    "visit_time": "2024-01-15T10:30:00",
    "channel": "main_gate",
    "auth_method": "face+fingerprint",
    "device_id": "DEV-001",
    "repeated_attempts_last_24h": 0,
    "multi_branch_same_day": 0
  }' | python3 -m json.tool

echo -e "\n3. High Risk Visit:"
curl -s -X POST "http://localhost:8000/evaluate-risk" \
  -H "Content-Type: application/json" \
  -d '{
    "visit_id": "VIS-TEST-002",
    "appointment_id": null,
    "national_id_hash": "ID-999999",
    "branch_id": "BR-001",
    "gate_id": "GATE-01",
    "visit_time": "2024-01-15T14:00:00",
    "channel": "side_gate",
    "auth_method": "manual_review",
    "device_id": "DEV-SUSPICIOUS",
    "repeated_attempts_last_24h": 8,
    "multi_branch_same_day": 1
  }' | python3 -m json.tool

echo -e "\n=========================================="
echo "  Tests Complete!"
echo "  Open http://localhost:8000/docs for interactive API"
echo "=========================================="

