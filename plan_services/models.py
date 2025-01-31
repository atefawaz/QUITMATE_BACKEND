from sqlalchemy import Column, Integer, String, Date, JSON
from .database import Base

class QuitPlan(Base):
    __tablename__ = "quit_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, nullable=False)
    start_date = Column(Date, nullable=False)
    quit_day = Column(Date, nullable=False)
    daily_targets = Column(JSON, nullable=False)  # Daily cigarette reduction
    strategies = Column(JSON, nullable=False)  # Personalized strategies
    reminders = Column(JSON, nullable=True)  # Notification reminders
