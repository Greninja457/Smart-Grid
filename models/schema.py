from pydantic import BaseModel
from datetime import datetime


class VoltageCreate(BaseModel):
    voltage_v: float
    rssi_dbm: int | None = None


class VoltageResponse(BaseModel):
    id: int
    voltage_v: float
    rssi_dbm: int | None
    recorded_at: datetime

    class Config:
        from_attributes = True


class HealthScoreResponse(BaseModel):
    health_score: int
    predicted_class: str

    stable_probability: float | None = None
    fluctuating_probability: float | None = None
    unstable_probability: float | None = None

    created_at: datetime

    class Config:
        from_attributes = True