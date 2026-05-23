# models.py — table prefix: build_a_full_stack_hospital_appointmentb
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Item(Base):
    __tablename__ = "build_a_full_stack_hospital_appointmentb_items"
    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String, index=True)
    description = Column(String, nullable=True)
    status      = Column(String, default="scheduled")
    doctor_name = Column(String, nullable=True)
    department  = Column(String, default="General")
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
