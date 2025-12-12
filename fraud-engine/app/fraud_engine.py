"""Core fraud detection engine with rule-based and ML-based scoring."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path

from app.config import (
    ISOLATION_FOREST_CONTAMINATION,
    ISOLATION_FOREST_RANDOM_STATE,
    RISK_THRESHOLD_LOW,
    RISK_THRESHOLD_MEDIUM,
    RISK_THRESHOLD_HIGH,
    RULE_WEIGHTS,
)
from app.schemas import RiskReason


class FraudEngine:
    """
    Fraud detection engine combining rule-based and ML-based approaches.
    
    Uses:
    - Rule-based scoring for interpretable risk factors
    - Isolation Forest for anomaly detection
    - Combined scoring for final risk assessment
    """
    
    def __init__(self):
        """Initialize the fraud engine."""
        self.model: IsolationForest = None
        self.scaler: StandardScaler = None
        self.is_trained = False
        self.feature_names = [
            "repeated_attempts_last_24h",
            "multi_branch_same_day",
            "device_reuse_score",
            "time_anomaly_score",
            "auth_method_risk",
            "visit_frequency_score",
        ]
    
    def _calculate_rule_based_features(self, visit_data: Dict) -> Dict[str, float]:
        """
        Calculate rule-based risk features.
        
        Args:
            visit_data: Dictionary with visit information
        
        Returns:
            Dictionary of feature values
        """
        features = {}
        
        # 1. Repeated attempts (normalized 0-1)
        attempts = visit_data.get("repeated_attempts_last_24h", 0)
        features["repeated_attempts_last_24h"] = min(attempts / 5.0, 1.0)
        
        # 2. Multi-branch same day (binary, but can be weighted)
        features["multi_branch_same_day"] = float(visit_data.get("multi_branch_same_day", 0))
        
        # 3. Device reuse score (would need historical data, simplified here)
        # In production, this would check how many different identities used same device
        device_id = visit_data.get("device_id", "")
        features["device_reuse_score"] = 0.0  # Placeholder, would be calculated from history
        
        # 4. Time anomaly score
        # Check if visit time is far from scheduled time (if appointment exists)
        appointment_id = visit_data.get("appointment_id")
        visit_time = visit_data.get("visit_time")
        
        if appointment_id and isinstance(visit_time, (str, datetime)):
            # In production, would fetch appointment time from DB
            # For now, assume 0 (no anomaly) if appointment exists
            features["time_anomaly_score"] = 0.0
        else:
            # No appointment = slightly higher risk
            features["time_anomaly_score"] = 0.3
        
        # 5. Auth method risk
        auth_method = visit_data.get("auth_method", "").lower()
        auth_risk_map = {
            "face+fingerprint": 0.0,
            "biometric_only": 0.1,
            "nafath": 0.3,
        }
        features["auth_method_risk"] = auth_risk_map.get(auth_method, 0.5)
        
        # 6. Visit frequency score (would need historical data)
        # Simplified: if many repeated attempts, frequency is high
        features["visit_frequency_score"] = min(attempts / 3.0, 1.0)
        
        return features
    
    def _calculate_rule_based_score(self, features: Dict[str, float]) -> Tuple[float, List[RiskReason]]:
        """
        Calculate rule-based risk score and reasons.
        
        Args:
            features: Dictionary of feature values
        
        Returns:
            Tuple of (score, list of reasons)
        """
        score = 0.0
        reasons = []
        
        # Repeated attempts
        if features["repeated_attempts_last_24h"] > 0:
            contrib = features["repeated_attempts_last_24h"] * RULE_WEIGHTS["repeated_attempts"]
            score += contrib
            if contrib > 0.1:
                reasons.append(RiskReason(
                    reason=f"Multiple attempts in last 24 hours ({features['repeated_attempts_last_24h']:.2f} normalized)",
                    contribution=contrib
                ))
        
        # Multi-branch same day
        if features["multi_branch_same_day"] > 0:
            contrib = features["multi_branch_same_day"] * RULE_WEIGHTS["multi_branch_same_day"]
            score += contrib
            reasons.append(RiskReason(
                reason="Multiple branches visited on same day",
                contribution=contrib
            ))
        
        # Device reuse (if calculated)
        if features["device_reuse_score"] > 0.2:
            contrib = features["device_reuse_score"] * RULE_WEIGHTS["device_reuse"]
            score += contrib
            reasons.append(RiskReason(
                reason="Device used by multiple identities",
                contribution=contrib
            ))
        
        # Time anomaly
        if features["time_anomaly_score"] > 0.2:
            contrib = features["time_anomaly_score"] * RULE_WEIGHTS["time_anomaly"]
            score += contrib
            reasons.append(RiskReason(
                reason="Visit time anomaly detected",
                contribution=contrib
            ))
        
        # Auth method
        if features["auth_method_risk"] > 0.3:
            contrib = features["auth_method_risk"] * RULE_WEIGHTS["auth_method_risk"]
            score += contrib
            reasons.append(RiskReason(
                reason=f"Higher risk authentication method: {features['auth_method_risk']:.2f}",
                contribution=contrib
            ))
        
        # Visit frequency
        if features["visit_frequency_score"] > 0.3:
            contrib = features["visit_frequency_score"] * RULE_WEIGHTS["visit_frequency"]
            score += contrib
            reasons.append(RiskReason(
                reason="Unusual visit frequency pattern",
                contribution=contrib
            ))
        
        return min(score, 1.0), reasons
    
    def _calculate_ml_score(self, features: Dict[str, float]) -> float:
        """
        Calculate ML-based anomaly score using Isolation Forest.
        
        Args:
            features: Dictionary of feature values
        
        Returns:
            Anomaly score (0-1, where 1 is more anomalous)
        """
        if not self.is_trained:
            return 0.5  # Default if model not trained
        
        # Convert features to array
        feature_array = np.array([[features[f] for f in self.feature_names]])
        
        # Scale features
        feature_array_scaled = self.scaler.transform(feature_array)
        
        # Get anomaly score (negative scores are anomalies)
        anomaly_score = self.model.score_samples(feature_array_scaled)[0]
        
        # Convert to 0-1 scale (more negative = more anomalous = higher risk)
        # Isolation Forest scores are typically in range [-0.5, 0.5]
        # Normalize to [0, 1] where 1 is most anomalous
        normalized_score = 1.0 - (anomaly_score + 0.5)  # Shift and invert
        
        return max(0.0, min(1.0, normalized_score))
    
    def train(self, visits_df: pd.DataFrame):
        """
        Train the Isolation Forest model on historical visit data.
        
        Args:
            visits_df: DataFrame with historical visits and features
        """
        print("Training fraud detection model...")
        
        # Calculate features for all visits
        feature_rows = []
        for _, row in visits_df.iterrows():
            visit_data = row.to_dict()
            features = self._calculate_rule_based_features(visit_data)
            feature_rows.append([features[f] for f in self.feature_names])
        
        X = np.array(feature_rows)
        
        # Train scaler
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Isolation Forest
        self.model = IsolationForest(
            contamination=ISOLATION_FOREST_CONTAMINATION,
            random_state=ISOLATION_FOREST_RANDOM_STATE,
            n_estimators=100,
        )
        self.model.fit(X_scaled)
        
        self.is_trained = True
        print("✓ Model trained successfully")
    
    def evaluate_risk(self, visit_data: Dict) -> Tuple[float, str, List[RiskReason]]:
        """
        Evaluate risk for a single visit.
        
        Args:
            visit_data: Dictionary with visit information
        
        Returns:
            Tuple of (risk_score, risk_level, reasons)
        """
        # Calculate features
        features = self._calculate_rule_based_features(visit_data)
        
        # Get rule-based score
        rule_score, rule_reasons = self._calculate_rule_based_score(features)
        
        # Get ML-based score
        ml_score = self._calculate_ml_score(features)
        
        # Combine scores (weighted average: 60% rules, 40% ML)
        combined_score = 0.6 * rule_score + 0.4 * ml_score
        
        # Add ML reason if significant
        if ml_score > 0.5:
            rule_reasons.append(RiskReason(
                reason=f"ML anomaly detection flagged this visit (score: {ml_score:.2f})",
                contribution=ml_score * 0.4
            ))
        
        # Determine risk level
        if combined_score >= RISK_THRESHOLD_HIGH:
            risk_level = "critical"
        elif combined_score >= RISK_THRESHOLD_MEDIUM:
            risk_level = "high"
        elif combined_score >= RISK_THRESHOLD_LOW:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return combined_score, risk_level, rule_reasons
    
    def get_ml_analysis(self, visit_data: Dict) -> Dict:
        """
        Get detailed ML analysis for a visit.
        
        Args:
            visit_data: Dictionary with visit information
        
        Returns:
            Dictionary with ML analysis details
        """
        features = self._calculate_rule_based_features(visit_data)
        
        # Get raw ML scores
        ml_score = self._calculate_ml_score(features)
        
        # Get anomaly prediction
        if self.is_trained:
            feature_array = np.array([[features[f] for f in self.feature_names]])
            feature_array_scaled = self.scaler.transform(feature_array)
            anomaly_score = self.model.score_samples(feature_array_scaled)[0]
            is_anomaly = self.model.predict(feature_array_scaled)[0] == -1
        else:
            anomaly_score = 0.0
            is_anomaly = False
        
        # Feature importance (based on deviation from normal)
        feature_importance = {}
        if self.is_trained:
            # Calculate how much each feature contributes to anomaly
            for i, feature_name in enumerate(self.feature_names):
                feature_value = features[feature_name]
                # Simple importance: higher values = more suspicious
                feature_importance[feature_name] = {
                    "value": round(feature_value, 4),
                    "contribution": round(feature_value * 100, 2),
                    "status": "high" if feature_value > 0.5 else "medium" if feature_value > 0.3 else "low"
                }
        
        return {
            "ml_score": round(ml_score, 4),
            "anomaly_score": round(anomaly_score, 4),
            "is_anomaly": bool(is_anomaly),
            "anomaly_probability": round((1 - (anomaly_score + 0.5)) * 100, 2) if self.is_trained else 0,
            "feature_analysis": feature_importance,
            "model_confidence": "high" if self.is_trained else "low",
            "model_type": "Isolation Forest",
            "features_used": self.feature_names
        }
    
    def get_ml_analysis(self, visit_data: Dict) -> Dict:
        """
        Get detailed ML analysis for expert fraud detection.
        
        Args:
            visit_data: Dictionary with visit information
        
        Returns:
            Dictionary with ML analysis details
        """
        features = self._calculate_rule_based_features(visit_data)
        ml_score = self._calculate_ml_score(features)
        rule_score, _ = self._calculate_rule_based_score(features)
        
        # Determine pattern type based on features
        pattern_type = "normal"
        pattern_details = []
        
        if features["repeated_attempts_last_24h"] > 0.6:
            pattern_type = "repeated_attempts"
            pattern_details.append(f"محاولات متكررة: {features['repeated_attempts_last_24h']:.2%}")
        
        if features["multi_branch_same_day"] > 0:
            pattern_type = "multi_branch"
            pattern_details.append("زيارات متعددة في فروع مختلفة")
        
        if features["device_reuse_score"] > 0.3:
            pattern_type = "device_reuse"
            pattern_details.append("استخدام أجهزة متعددة")
        
        if features["time_anomaly_score"] > 0.3:
            pattern_type = "time_anomaly"
            pattern_details.append("شذوذ في التوقيت")
        
        if features["auth_method_risk"] > 0.5:
            pattern_type = "weak_auth"
            pattern_details.append("طريقة مصادقة ضعيفة")
        
        if ml_score > 0.7:
            pattern_type = "ml_anomaly"
            pattern_details.append("نمط شاذ اكتشفه ML")
        
        # Feature importance
        feature_importance = {
            "repeated_attempts": features["repeated_attempts_last_24h"],
            "multi_branch": features["multi_branch_same_day"],
            "device_reuse": features["device_reuse_score"],
            "time_anomaly": features["time_anomaly_score"],
            "auth_method": features["auth_method_risk"],
            "visit_frequency": features["visit_frequency_score"],
        }
        
        return {
            "ml_anomaly_score": round(ml_score, 4),
            "rule_based_score": round(rule_score, 4),
            "combined_score": round(0.6 * rule_score + 0.4 * ml_score, 4),
            "pattern_type": pattern_type,
            "pattern_details": pattern_details,
            "feature_importance": feature_importance,
            "is_anomaly": ml_score > 0.5,
            "confidence": round(ml_score * 100, 1),
        }


# Global instance (singleton pattern)
_fraud_engine_instance = None


def get_fraud_engine() -> FraudEngine:
    """Get or create the global fraud engine instance."""
    global _fraud_engine_instance
    if _fraud_engine_instance is None:
        _fraud_engine_instance = FraudEngine()
    return _fraud_engine_instance

