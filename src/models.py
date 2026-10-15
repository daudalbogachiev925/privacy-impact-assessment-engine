from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, validator

class DataAsset(BaseModel):
    name: str = Field(..., description="Human readable name of the data asset")
    description: Optional[str] = None
    sensitivity: str = Field(..., description="Sensitivity level: low, medium, high")
    owner_email: EmailStr = Field(..., description="Contact email of the data owner")

    @validator('sensitivity')
    def check_sensitivity(cls, v: str) -> str:
        allowed = {'low', 'medium', 'high'}
        if v.lower() not in allowed:
            raise ValueError(f"sensitivity must be one of {allowed}")
        return v.lower()

class Impact(BaseModel):
    asset: DataAsset
    risk_score: int = Field(..., ge=0, le=100, description="Calculated risk score (0‑100)")
    justification: str

class AssessmentReport(BaseModel):
    impacts: List[Impact]
    summary: str
