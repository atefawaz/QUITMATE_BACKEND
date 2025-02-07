from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY  # ✅ Corrected Import
from sqlalchemy.sql import func
from questionnaire_services.database import Base

class Questionnaire(Base):
    __tablename__ = "questionnaire"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False)  # ✅ Keep track of unique users
    daily_cigarettes = Column(Integer, nullable=False)
    quitting_speed = Column(String, nullable=False)  

    high_risk_times = Column(ARRAY(String), nullable=True)  # ✅ Native ARRAY (No need for serialization hacks)
    notification_preference = Column(String, nullable=False)
    first_cigarette_time = Column(String, nullable=False)

    smoking_triggers = Column(ARRAY(String), nullable=True)
    previous_quit_attempts = Column(Boolean, nullable=False)
    previous_methods = Column(ARRAY(String), nullable=True)

    health_goals = Column(ARRAY(String), nullable=True)
    preferred_timeline = Column(String, nullable=False)
    smoking_context = Column(ARRAY(String), nullable=True)

    created_at = Column(DateTime, server_default=func.now())  # ✅ Automatically set timestamp

