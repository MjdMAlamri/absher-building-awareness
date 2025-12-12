"""Pydantic models for request/response validation."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class RiskEvaluationRequest(BaseModel):
    """Request model for risk evaluation endpoint."""
    
    visit_id: str = Field(..., description="Unique visit identifier")
    appointment_id: Optional[str] = Field(None, description="Associated appointment ID")
    national_id_hash: str = Field(..., description="Hashed national ID")
    branch_id: str = Field(..., description="Branch identifier")
    gate_id: str = Field(..., description="Gate identifier")
    visit_time: datetime = Field(..., description="Visit timestamp (ISO8601)")
    channel: str = Field(..., description="Entry channel (e.g., 'main_gate', 'side_gate')")
    auth_method: str = Field(..., description="Authentication method used")
    device_id: Optional[str] = Field(None, description="Device identifier")
    repeated_attempts_last_24h: int = Field(0, ge=0, description="Attempts in last 24 hours")
    multi_branch_same_day: int = Field(0, ge=0, le=1, description="1 if visited multiple branches same day")
    
    class Config:
        json_schema_extra = {
            "example": {
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
                "multi_branch_same_day": 0,
            }
        }


class RiskReason(BaseModel):
    """Individual risk reason with score contribution."""
    
    reason: str = Field(..., description="Description of the risk factor")
    contribution: float = Field(..., ge=0, le=1, description="Contribution to risk score (0-1)")


class RiskEvaluationResponse(BaseModel):
    """Response model for risk evaluation endpoint."""
    
    visit_id: str
    risk_score: float = Field(..., ge=0, le=1, description="Overall risk score (0-1)")
    risk_level: str = Field(..., description="Risk level: 'low', 'medium', 'high', 'critical'")
    reasons: List[RiskReason] = Field(..., description="List of risk factors identified")
    model_version: str = Field(default="1.0.0", description="Model version used")
    
    class Config:
        protected_namespaces = ()
        json_schema_extra = {
            "example": {
                "visit_id": "VIS-001",
                "risk_score": 0.45,
                "risk_level": "medium",
                "reasons": [
                    {"reason": "Multiple attempts in last 24 hours", "contribution": 0.25},
                    {"reason": "Time anomaly detected", "contribution": 0.20}
                ],
                "model_version": "1.0.0"
            }
        }

