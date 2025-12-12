"""Demo script to show example outputs from the fraud detection service."""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def demo_request(visit_data, description):
    """Make a request and display the result."""
    print(f"\n📋 {description}")
    print(f"Request: {json.dumps(visit_data, indent=2, default=str)}")
    
    try:
        response = requests.post(f"{BASE_URL}/evaluate-risk", json=visit_data, timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Response:")
            print(f"   Risk Score: {result['risk_score']:.4f}")
            print(f"   Risk Level: {result['risk_level'].upper()}")
            print(f"   Reasons ({len(result['reasons'])}):")
            for reason in result['reasons']:
                print(f"     • {reason['reason']} (contribution: {reason['contribution']:.3f})")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the server is running:")
        print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run demo examples."""
    print_section("Fraud Detection Service - Demo Examples")
    print("\n⚠️  Note: This is a demonstration. Some features may need")
    print("   additional data sources or database connections for full functionality.")
    
    # Example 1: Low Risk Visit
    demo_request({
        "visit_id": "VIS-DEMO-001",
        "appointment_id": "APT-001",
        "national_id_hash": "ID-123456",
        "branch_id": "BR-001",
        "gate_id": "GATE-01",
        "visit_time": datetime.now().isoformat(),
        "channel": "main_gate",
        "auth_method": "face+fingerprint",
        "device_id": "DEV-001",
        "repeated_attempts_last_24h": 0,
        "multi_branch_same_day": 0,
    }, "Example 1: Normal Visit (Low Risk)")
    
    # Example 2: Medium Risk - Multiple Attempts
    demo_request({
        "visit_id": "VIS-DEMO-002",
        "appointment_id": "APT-002",
        "national_id_hash": "ID-789012",
        "branch_id": "BR-002",
        "gate_id": "GATE-02",
        "visit_time": datetime.now().isoformat(),
        "channel": "side_gate",
        "auth_method": "qr+otp",
        "device_id": "DEV-002",
        "repeated_attempts_last_24h": 3,
        "multi_branch_same_day": 0,
    }, "Example 2: Multiple Attempts (Medium Risk)")
    
    # Example 3: High Risk - Multiple Branches Same Day
    demo_request({
        "visit_id": "VIS-DEMO-003",
        "appointment_id": None,
        "national_id_hash": "ID-345678",
        "branch_id": "BR-003",
        "gate_id": "GATE-03",
        "visit_time": datetime.now().isoformat(),
        "channel": "main_gate",
        "auth_method": "manual_review",
        "device_id": "DEV-003",
        "repeated_attempts_last_24h": 2,
        "multi_branch_same_day": 1,
    }, "Example 3: Suspicious Pattern (High Risk)")
    
    # Example 4: Critical Risk - All Red Flags
    demo_request({
        "visit_id": "VIS-DEMO-004",
        "appointment_id": None,
        "national_id_hash": "ID-999999",
        "branch_id": "BR-001",
        "gate_id": "GATE-01",
        "visit_time": datetime.now().isoformat(),
        "channel": "side_gate",
        "auth_method": "manual_review",
        "device_id": "DEV-SUSPICIOUS",
        "repeated_attempts_last_24h": 8,
        "multi_branch_same_day": 1,
    }, "Example 4: Critical Risk - All Red Flags")
    
    print_section("Demo Complete")
    print("\n💡 To run the full service:")
    print("   1. Generate data: python -m app.data_generator")
    print("   2. Start server: uvicorn app.main:app --reload")
    print("   3. Run demo: python demo.py")
    print("\n📝 Note: Current implementation uses simplified features.")
    print("   For production, connect to database for historical data lookup.")

if __name__ == "__main__":
    main()

