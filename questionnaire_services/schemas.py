from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class QuestionnaireCreate(BaseModel):
    daily_cigarettes: int
    quitting_speed: str  # gradual, cold_turkey, assisted, tapering_off
    high_risk_times: List[str]  # morning, after_meals, social_events, work_stress, etc.
    notification_preference: str  # email, sms, app_push, none
    first_cigarette_time: str  # "HH:MM" format
    smoking_triggers: List[str]  # stress, boredom, peer_pressure, alcohol, coffee, driving
    previous_quit_attempts: bool
    previous_methods: List[str]  # nicotine_patch, therapy, vaping, medication, support_groups
    health_goals: List[str]  # improve_lung_health, fitness, save_money, better_sleep
    preferred_timeline: str  # 1 month, 3 months, 6 months, flexible
    smoking_context: List[str]  # social_gatherings, alone, work_breaks, studying


class QuestionnaireResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime  
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
            datetime: lambda v: v.isoformat() 
        }