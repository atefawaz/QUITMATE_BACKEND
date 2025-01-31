from pydantic import BaseModel
from typing import List
import datetime

class PlanResponse(BaseModel):
    user_id: int
    start_date: datetime.date
    quit_day: datetime.date
    daily_targets: List[int]
    strategies: List[str]
    reminders: List[str]

    class Config:
        orm_mode = True
