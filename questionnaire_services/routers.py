from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from questionnaire_services.database import get_db
from questionnaire_services.models import Questionnaire
from questionnaire_services.schemas import QuestionnaireCreate, QuestionnaireResponse
from questionnaire_services.config import settings  # Configuration for JWT settings

router = APIRouter(prefix="/questionnaire", tags=["Questionnaire"])

def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT token
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        print(f"Decoded payload: {payload}")  # Debugging log
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError as e:
        print(f"JWT Error: {e}")  # Debugging log
        raise credentials_exception

@router.post("/", response_model=QuestionnaireResponse)
@router.post("/", response_model=QuestionnaireResponse)
def submit_questionnaire(
    request: Request,
    questionnaire: QuestionnaireCreate,
    db: Session = Depends(get_db)
):
    # Extract the token from the Authorization header
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing or invalid",
        )

    # Remove "Bearer " prefix from the token
    token = token.replace("Bearer ", "")
    user_id = get_current_user(token)

    # Create a new questionnaire entry
    new_questionnaire = Questionnaire(
        user_id=user_id,
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

    # Serialize the response
    return QuestionnaireResponse.from_orm_with_serialization(new_questionnaire)
