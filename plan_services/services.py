import requests
import datetime
from sqlalchemy.orm import Session
from datetime import date, timedelta
from .models import QuitPlan

# Questionnaire Service URL
QUESTIONNAIRE_SERVICE_URL = "http://localhost:8001/questionnaire"

def fetch_user_questionnaire(user_id: int, token: str):
    """Fetch user's questionnaire from the service"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{QUESTIONNAIRE_SERVICE_URL}/{user_id}", headers=headers)

    if response.status_code != 200:
        return None

    return response.json()


def calculate_quit_timeline(daily_cigarettes, quitting_speed):
    """Dynamic quitting plan based on smoking level & chosen method"""
    
    daily_targets = []
    days_to_reduce = 0

    if quitting_speed == "gradual":
        if daily_cigarettes <= 10:
            days_to_reduce = 90  # ~3 months
        elif 10 < daily_cigarettes <= 20:
            days_to_reduce = 120  # ~4 months
        else:
            days_to_reduce = 180  # ~6 months

        reduction_step = max(1, daily_cigarettes // (days_to_reduce // 10))

        for day in range(1, days_to_reduce + 1):
            if day % 10 == 0 and daily_cigarettes > 0:
                daily_cigarettes -= reduction_step
            daily_targets.append(max(daily_cigarettes, 0))

    elif quitting_speed == "cold_turkey":
        days_to_reduce = 28  # 4 weeks total (realistic)
        for day in range(1, days_to_reduce + 1):
            if day <= 7:
                daily_cigarettes = max(1, daily_cigarettes // 2)
            elif 7 < day <= 14:
                daily_cigarettes = max(1, daily_cigarettes // 3)
            elif 14 < day <= 21:
                daily_cigarettes = max(1, daily_cigarettes // 4)
            else:
                daily_cigarettes = 0  
            daily_targets.append(daily_cigarettes)

    return daily_targets, days_to_reduce


def generate_personalized_strategies(smoking_triggers, quitting_speed):
    """Create strategies based on user data"""

    strategies = []

    if quitting_speed == "cold_turkey":
        strategies.append("Use nicotine patches or gum to manage cravings.")
        strategies.append("Drink lots of water to flush out nicotine faster.")

    if "stress" in smoking_triggers:
        strategies.append("Practice meditation or deep breathing when stressed.")

    if "habit" in smoking_triggers:
        strategies.append("Replace smoking with chewing gum or snacking on nuts.")

    if "peer_pressure" in smoking_triggers:
        strategies.append("Avoid smoking environments and prepare responses for social situations.")

    return strategies


def generate_motivational_reminders(days_to_reduce):
    """Generate motivational reminders based on timeline"""
    reminders = []

    reminders.append("🚀 Stay strong! Every cigarette avoided helps your lungs recover.")
    
    if days_to_reduce > 90:
        reminders.append("💪 Long-term commitment = long-term health benefits!")

    reminders.append("💰 You're saving money—track your progress!")

    return reminders


def create_quit_plan(user_id: int, token: str, db: Session):
    """Main function to generate a personalized quitting plan"""
    
    user_data = fetch_user_questionnaire(user_id, token)
    if not user_data:
        return None  

    # Generate quitting plan
    daily_reduction, total_days = calculate_quit_timeline(
        user_data["daily_cigarettes"], 
        user_data["quitting_speed"]
    )

    personalized_strategies = generate_personalized_strategies(user_data["smoking_triggers"], user_data["quitting_speed"])
    reminders = generate_motivational_reminders(total_days)

    # Store plan in DB
    new_plan = QuitPlan(
        user_id=user_id,
        start_date=date.today(),
        quit_day=date.today() + timedelta(days=total_days),
        daily_targets=daily_reduction,
        strategies=personalized_strategies,
        reminders=reminders
    )

    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)

    return new_plan
