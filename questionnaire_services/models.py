from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, func
from questionnaire_services.database import Base


class Questionnaire(Base):
    __tablename__ = "questionnaire"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    daily_cigarettes = Column(Integer, nullable=False)
    quitting_speed = Column(String, nullable=False)
    high_risk_times_raw = Column("high_risk_times", String)  # Stored as a comma-separated string
    notification_preference = Column(String, nullable=False)
    first_cigarette_time = Column(String, nullable=False)
    smoking_triggers_raw = Column("smoking_triggers", Text)  # Stored as a comma-separated string
    previous_quit_attempts = Column(Boolean, nullable=False)
    previous_methods_raw = Column("previous_methods", Text)  # Stored as a comma-separated string
    health_goals_raw = Column("health_goals", Text)  # Stored as a comma-separated string
    preferred_timeline = Column(String, nullable=False)
    smoking_context_raw = Column("smoking_context", Text)  # Stored as a comma-separated string
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Serialize and deserialize list fields
    @property
    def high_risk_times(self):
        return self.high_risk_times_raw.split(",") if self.high_risk_times_raw else []

    @high_risk_times.setter
    def high_risk_times(self, value):
        self.high_risk_times_raw = ",".join(value) if value else None

    @property
    def smoking_triggers(self):
        return self.smoking_triggers_raw.split(",") if self.smoking_triggers_raw else []

    @smoking_triggers.setter
    def smoking_triggers(self, value):
        self.smoking_triggers_raw = ",".join(value) if value else None

    @property
    def previous_methods(self):
        return self.previous_methods_raw.split(",") if self.previous_methods_raw else []

    @previous_methods.setter
    def previous_methods(self, value):
        self.previous_methods_raw = ",".join(value) if value else None

    @property
    def health_goals(self):
        return self.health_goals_raw.split(",") if self.health_goals_raw else []

    @health_goals.setter
    def health_goals(self, value):
        self.health_goals_raw = ",".join(value) if value else None

    @property
    def smoking_context(self):
        return self.smoking_context_raw.split(",") if self.smoking_context_raw else []

    @smoking_context.setter
    def smoking_context(self, value):
        self.smoking_context_raw = ",".join(value) if value else None
