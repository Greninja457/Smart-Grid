from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    Double,
    String,
    DateTime,
    Computed
)

from sqlalchemy.sql import func

from lib.db_conn import Base


class VoltageReading(Base):
    __tablename__ = "voltage_readings"

    id = Column(BigInteger, primary_key=True, index=True)

    voltage_v = Column(Double, nullable=False)

    rssi_dbm = Column(Integer)

    recorded_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


class OutageEvent(Base):
    __tablename__ = "outage_events"

    id = Column(BigInteger, primary_key=True, index=True)

    started_at = Column(
        DateTime(timezone=True),
        nullable=False
    )

    ended_at = Column(
        DateTime(timezone=True)
    )

    duration_seconds = Column(
        Integer,
        Computed("""
            CASE
                WHEN ended_at IS NOT NULL
                THEN EXTRACT(EPOCH FROM (ended_at - started_at))::INTEGER
                ELSE NULL
            END
        """)
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class GridHealthScore(Base):
    __tablename__ = "grid_health_scores"

    id = Column(BigInteger, primary_key=True, index=True)

    health_score = Column(Integer, nullable=False)

    predicted_class = Column(String(32), nullable=False)

    stable_probability = Column(Double)

    fluctuating_probability = Column(Double)

    unstable_probability = Column(Double)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )