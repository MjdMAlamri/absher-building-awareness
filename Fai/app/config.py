"""Configuration constants for the fraud detection service."""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Data directories
SAMPLE_DATA_DIR = BASE_DIR / "sample_data"
SAMPLE_DATA_DIR.mkdir(exist_ok=True)

# File paths
APPOINTMENTS_CSV = SAMPLE_DATA_DIR / "appointments.csv"
VISITS_CSV = SAMPLE_DATA_DIR / "visits.csv"

# Model parameters
ISOLATION_FOREST_CONTAMINATION = 0.1  # Expected proportion of outliers
ISOLATION_FOREST_RANDOM_STATE = 42

# Risk thresholds
RISK_THRESHOLD_LOW = 0.3
RISK_THRESHOLD_MEDIUM = 0.6
RISK_THRESHOLD_HIGH = 0.8

# Feature weights for rule-based scoring
RULE_WEIGHTS = {
    "repeated_attempts": 0.25,
    "multi_branch_same_day": 0.20,
    "device_reuse": 0.20,
    "time_anomaly": 0.15,
    "auth_method_risk": 0.10,
    "visit_frequency": 0.10,
}

