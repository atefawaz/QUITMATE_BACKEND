from pydantic import BaseModel
from typing import List
from datetime import datetime


class QuestionnaireCreate(BaseModel):
    daily_cigarettes: int
    quitting_speed: str
    high_risk_times: List[str]
    notification_preference: str
    first_cigarette_time: str
    smoking_triggers: List[str]
    previous_quit_attempts: bool
    previous_methods: List[str]
    health_goals: List[str]
    preferred_timeline: str
    smoking_context: List[str]


class QuestionnaireResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime  # ✅ This now correctly handles datetime
    daily_cigarettes: int
    quitting_speed: str
    high_risk_times: List[str]
    notification_preference: str
    first_cigarette_time: str
    smoking_triggers: List[str]
    previous_quit_attempts: bool
    previous_methods: List[str]
    health_goals: List[str]
    preferred_timeline: str
    smoking_context: List[str]

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()  # ✅ Serialize datetime as ISO 8601 string
        }