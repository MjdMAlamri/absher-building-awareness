"""Unit tests for fraud detection engine."""

import pytest
from datetime import datetime
from app.fraud_engine import FraudEngine
from app.schemas import RiskEvaluationRequest


def test_fraud_engine_initialization():
    """Test that fraud engine initializes correctly."""
    engine = FraudEngine()
    assert engine.model is None or engine.is_trained is False
    assert engine.feature_names is not None


def test_rule_based_scoring_low_risk():
    """Test rule-based scoring for low-risk visit."""
    engine = FraudEngine()
    
    visit_data = {
        "visit_id": "VIS-001",
        "national_id_hash": "ID-123456",
        "branch_id": "BR-001",
        "gate_id": "GATE-01",
        "visit_time": datetime.now(),
        "channel": "main_gate",
        "auth_method": "face+fingerprint",
        "device_id": "DEV-001",
        "repeated_attempts_last_24h": 0,
        "multi_branch_same_day": 0,
    }
    
    features = engine._calculate_rule_based_features(visit_data)
    score, reasons = engine._calculate_rule_based_score(features)
    
    assert score < 0.3  # Should be low risk
    assert isinstance(reasons, list)


def test_rule_based_scoring_high_risk():
    """Test rule-based scoring for high-risk visit."""
    engine = FraudEngine()
    
    visit_data = {
        "visit_id": "VIS-002",
        "national_id_hash": "ID-123456",
        "branch_id": "BR-001",
        "gate_id": "GATE-01",
        "visit_time": datetime.now(),
        "channel": "main_gate",
        "auth_method": "manual_review",
        "device_id": "DEV-001",
        "repeated_attempts_last_24h": 5,
        "multi_branch_same_day": 1,
    }
    
    features = engine._calculate_rule_based_features(visit_data)
    score, reasons = engine._calculate_rule_based_score(features)
    
    assert score > 0.5  # Should be higher risk
    assert len(reasons) > 0  # Should have risk reasons


def test_evaluate_risk():
    """Test full risk evaluation."""
    engine = FraudEngine()
    
    visit_data = {
        "visit_id": "VIS-003",
        "national_id_hash": "ID-789012",
        "branch_id": "BR-002",
        "gate_id": "GATE-02",
        "visit_time": datetime.now(),
        "channel": "side_gate",
        "auth_method": "qr+otp",
        "device_id": "DEV-002",
        "repeated_attempts_last_24h": 2,
        "multi_branch_same_day": 0,
    }
    
    risk_score, risk_level, reasons = engine.evaluate_risk(visit_data)
    
    assert 0 <= risk_score <= 1
    assert risk_level in ["low", "medium", "high", "critical"]
    assert isinstance(reasons, list)

