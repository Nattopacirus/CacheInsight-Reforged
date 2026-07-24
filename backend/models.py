import uuid
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Preset(Base):
    __tablename__ = "presets"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    cache_size = Column(Integer, nullable=False)
    block_size = Column(Integer, nullable=False)
    mapping_type = Column(String(50), nullable=False)
    n_way = Column(Integer, nullable=True)
    replacement_policy = Column(String(50), nullable=False, default="LRU")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SimulationJob(Base):
    __tablename__ = "simulation_jobs"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    status = Column(String(50), default="Pending")
    progress = Column(Integer, default=0)
    result = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
