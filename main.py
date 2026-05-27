from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from lib.db_conn import engine, get_db
from models.models import (
    Base,
    VoltageReading,
    GridHealthScore
)

from models.schema import (
    VoltageCreate,
    VoltageResponse,
    HealthScoreResponse
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Smart Grid Edge Monitor Backend Running"
    }


@app.post(
    "/api/v1/data",
    response_model=VoltageResponse
)
def insert_voltage(
    payload: VoltageCreate,
    db: Session = Depends(get_db)
):

    voltage = VoltageReading(
        voltage_v=payload.voltage_v,
        rssi_dbm=payload.rssi_dbm
    )

    db.add(voltage)

    db.commit()

    db.refresh(voltage)

    return voltage


@app.get("/api/v1/voltage")
def get_voltage_readings(
    limit: int = 100,
    db: Session = Depends(get_db)
):

    readings = (
        db.query(VoltageReading)
        .order_by(
            VoltageReading.recorded_at.desc()
        )
        .limit(limit)
        .all()
    )

    return readings


@app.get(
    "/api/v1/health-score",
    response_model=HealthScoreResponse
)
def get_latest_health_score(
    db: Session = Depends(get_db)
):

    score = (
        db.query(GridHealthScore)
        .order_by(
            GridHealthScore.created_at.desc()
        )
        .first()
    )

    return score