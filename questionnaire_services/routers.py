import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from questionnaire_services.database import get_db
from questionnaire_services.models import Questionnaire
from questionnaire_services.schemas import QuestionnaireCreate, QuestionnaireResponse
from auth_services.services.auth import get_current_user
from auth_services.models import User

router = APIRouter()

@router.post("/submit", response_model=QuestionnaireResponse)
def submit_questionnaire(
    questionnaire: QuestionnaireCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # ✅ Check if the user already has a questionnaire
    existing_questionnaire = db.query(Questionnaire).filter(Questionnaire.user_id == current_user.id).first()
    if existing_questionnaire:
        raise HTTPException(status_code=400, detail="User has already submitted a questionnaire.")

    # ✅ Store the questionnaire in the database
    new_questionnaire = Questionnaire(**questionnaire.dict(), user_id=current_user.id)
    db.add(new_questionnaire)
    db.commit()
    db.refresh(new_questionnaire)

    # ✅ Trigger quitting plan generation
    plan_response = requests.post(
        "http://127.0.0.1:8002/plan/generate_plan",
        headers={"Authorization": f"Bearer {current_user.token}"}  # Ensure token is sent
    )

    if plan_response.status_code != 200:
        print(f"❌ Failed to generate plan. Response: {plan_response.json()}")
        raise HTTPException(status_code=400, detail="Plan generation failed")

    print(f"✅ Quit plan generated successfully for user {current_user.id}")

    return new_questionnaire


@router.get("/{user_id}")
def get_questionnaire(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    questionnaire = db.query(Questionnaire).filter(Questionnaire.user_id == user_id).first()
    if not questionnaire:
        raise HTTPException(status_code=404, detail="Questionnaire not found")
    return questionnaire
