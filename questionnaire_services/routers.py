from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from questionnaire_services.database import get_db
from questionnaire_services.models import Questionnaire
from questionnaire_services.schemas import QuestionnaireCreate, QuestionnaireResponse
from auth_services.services.auth import get_current_user
from auth_services.models import User
from fastapi.responses import JSONResponse
import logging

router = APIRouter()

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@router.post("/submit", response_model=QuestionnaireResponse)
def submit_questionnaire(
    questionnaire: QuestionnaireCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        logger.info(f"Submitting questionnaire for user {current_user.id}")

        new_questionnaire = Questionnaire(
            user_id=current_user.id,
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
        )

        db.add(new_questionnaire)
        db.commit()
        db.refresh(new_questionnaire)

        # ✅ Convert SQLAlchemy model to a serializable dictionary
        response_content = {
            "id": new_questionnaire.id,
            "user_id": new_questionnaire.user_id,
            "daily_cigarettes": new_questionnaire.daily_cigarettes,
            "quitting_speed": new_questionnaire.quitting_speed,
            "high_risk_times": new_questionnaire.high_risk_times,
            "notification_preference": new_questionnaire.notification_preference,
            "first_cigarette_time": str(new_questionnaire.first_cigarette_time),  # Convert datetime to string
            "smoking_triggers": new_questionnaire.smoking_triggers,
            "previous_quit_attempts": new_questionnaire.previous_quit_attempts,
            "previous_methods": new_questionnaire.previous_methods,
            "health_goals": new_questionnaire.health_goals,
            "preferred_timeline": new_questionnaire.preferred_timeline,
            "smoking_context": new_questionnaire.smoking_context,
            "created_at": new_questionnaire.created_at.isoformat()  # Convert datetime to string
        }

        # ✅ Return a proper JSON response
        return JSONResponse(content=response_content)

    except Exception as e:
        logger.error(f"Error submitting questionnaire: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
