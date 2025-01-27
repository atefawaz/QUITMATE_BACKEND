from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class QuestionnaireCreate(BaseModel):
    daily_cigarettes: int
    quitting_speed: str
    high_risk_times: Optional[List[str]] = None
    notification_preference: str
    first_cigarette_time: str
    smoking_triggers: Optional[List[str]] = None
    previous_quit_attempts: bool
    previous_methods: Optional[List[str]] = None
    health_goals: Optional[List[str]] = None
    preferred_timeline: str
    smoking_context: Optional[List[str]] = None

class QuestionnaireResponse(QuestionnaireCreate):
    id: int
    user_id: int
    created_at: str  # Change type to string for proper serialization

    class Config:
        orm_mode = True

    @staticmethod
    def from_orm_with_serialization(questionnaire):
        """
        Serialize the response, converting datetime to ISO 8601 string.
        """
        return QuestionnaireResponse(
            id=questionnaire.id,
            user_id=questionnaire.user_id,
            daily_cigarettes=questionnaire.daily_cigarettes,
            quitting_speed=questionnaire.quitting_speed,
            high_risk_times=questionnaire.high_risk_times,
            notification_preference=questionnaire.notification_preference,
            first_cigarette_time=questionnaire.first_cigarette_time,
            smoking_triggers=questionnaire.smoking_triggers,
            previous_quit_attempts=questionnaire.previous_quit_attempts,
            previous_methods=questionnaire.previous_methods,
            health_goals=questionnaire.health_goals,
            preferred_timeline=questionnaire.preferred_timeline,
            smoking_context=questionnaire.smoking_context,
            created_at=questionnaire.created_at.isoformat()  # Serialize datetime to ISO format
        )
