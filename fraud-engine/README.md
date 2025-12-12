# Fraud Detection Service

AI-powered fraud detection microservice for Smart Gate & أبشر system.

## Features

- **Synthetic Data Generation**: Generate realistic appointments and visits data
- **Rule-Based Detection**: Interpretable risk scoring based on business rules
- **ML-Based Detection**: Isolation Forest for anomaly detection
- **RESTful API**: Easy-to-use FastAPI endpoint for risk evaluation
- **Production-Ready**: Clean structure, type hints, and comprehensive error handling

## Project Structure

```
fraud_service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app & /evaluate-risk endpoint
│   ├── fraud_engine.py      # Core fraud logic & ML model
│   ├── schemas.py           # Pydantic models (request/response)
│   ├── data_generator.py    # Synthetic data generator
│   └── config.py            # Configuration constants
├── sample_data/             # Generated CSVs (created on first run)
│   ├── appointments.csv
│   └── visits.csv
├── tests/
│   └── test_fraud_engine.py # Unit tests
├── requirements.txt
├── demo.py                  # Demo script with examples
└── README.md
```

## Installation

1. **Create virtual environment** (Python 3.11+):
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Generate synthetic data**:
```bash
cd fraud_service
python -m app.data_generator
```

This will create:
- `sample_data/appointments.csv` (~5,000 appointments)
- `sample_data/visits.csv` (~20,000 visits)

## Usage

### Start the API Server

```bash
cd fraud_service
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

### Evaluate Risk (Example)

**cURL**:
```bash
curl -X POST "http://localhost:8000/evaluate-risk" \
  -H "Content-Type: application/json" \
  -d '{
    "visit_id": "VIS-001",
    "appointment_id": "APT-001",
    "national_id_hash": "abc123def456",
    "branch_id": "BR-001",
    "gate_id": "GATE-01",
    "visit_time": "2024-01-15T10:30:00",
    "channel": "main_gate",
    "auth_method": "face+fingerprint",
    "device_id": "DEV-001",
    "repeated_attempts_last_24h": 0,
    "multi_branch_same_day": 0
  }'
```

**Python**:
```python
import requests

response = requests.post(
    "http://localhost:8000/evaluate-risk",
    json={
        "visit_id": "VIS-001",
        "national_id_hash": "abc123def456",
        "branch_id": "BR-001",
        "gate_id": "GATE-01",
        "visit_time": "2024-01-15T10:30:00",
        "channel": "main_gate",
        "auth_method": "face+fingerprint",
        "device_id": "DEV-001",
        "repeated_attempts_last_24h": 0,
        "multi_branch_same_day": 0,
    }
)

result = response.json()
print(f"Risk Score: {result['risk_score']}")
print(f"Risk Level: {result['risk_level']}")
print(f"Reasons: {result['reasons']}")
```

**Response**:
```json
{
  "visit_id": "VIS-001",
  "risk_score": 0.1234,
  "risk_level": "low",
  "reasons": [],
  "model_version": "1.0.0"
}
```

### Run Demo Script

```bash
cd fraud_service
python demo.py
```

This will show example requests and responses for different risk scenarios.

## Risk Levels

- **low**: risk_score < 0.3
- **medium**: 0.3 ≤ risk_score < 0.6
- **high**: 0.6 ≤ risk_score < 0.8
- **critical**: risk_score ≥ 0.8

## Risk Factors

The engine evaluates multiple risk factors:

1. **Repeated Attempts**: Multiple visits in last 24 hours
2. **Multi-Branch Same Day**: Same identity visiting multiple branches
3. **Device Reuse**: Same device used by multiple identities
4. **Time Anomaly**: Visit time far from scheduled appointment
5. **Auth Method**: Risk level of authentication method used
6. **Visit Frequency**: Unusual patterns in visit frequency
7. **ML Anomaly**: Isolation Forest detects anomalous patterns

## Testing

Run unit tests:
```bash
cd fraud_service
pytest tests/
```

## Integration with Smart Gate

The Smart Gate service can call `/evaluate-risk` when processing a visit:

```python
# In Smart Gate service
import requests

def check_visit_risk(visit_data):
    response = requests.post(
        "http://fraud-service:8000/evaluate-risk",
        json=visit_data,
        timeout=2.0
    )
    result = response.json()
    
    if result["risk_level"] in ["high", "critical"]:
        # Flag for manual review
        return "REVIEW_REQUIRED"
    elif result["risk_level"] == "medium":
        # Additional verification
        return "VERIFY"
    else:
        # Proceed normally
        return "APPROVED"
```

## Configuration

Edit `app/config.py` to adjust:
- Risk thresholds
- Feature weights
- Model parameters

## Notes

- The model trains on startup using `sample_data/visits.csv`
- In production, connect to a real database instead of CSV files
- Device reuse and time anomaly features are simplified; enhance with historical data lookup
- Isolation Forest contamination rate is set to 0.1 (10% expected outliers)

## ⚠️ Current Limitations (For Demo)

This is a working demo system. For production use, consider:

1. **Database Integration**: Replace CSV files with real database connections
2. **Historical Data Lookup**: Implement proper device reuse and time anomaly calculations
3. **Authentication**: Add API keys or OAuth for security
4. **Logging & Monitoring**: Add comprehensive logging and metrics
5. **Model Retraining**: Implement periodic model retraining pipeline
6. **Caching**: Add Redis for frequently accessed data

## License

MIT

