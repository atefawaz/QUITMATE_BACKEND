import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from plan_services.database import get_db
from plan_services.models import QuitPlan
from plan_services.schemas import PlanResponse
from plan_services.services import create_quit_plan
from auth_services.services.auth import get_current_user

router = APIRouter()

# ✅ Fix: Initialize logger in `plan_routes.py`
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/generate_plan", response_model=PlanResponse)
def generate_plan(
    db: Session = Depends(get_db),  
    current_user = Depends(get_current_user)
):
    """Generate and save a personalized quitting plan"""
    logger.info(f"📢 Generating plan for user {current_user.id}")

    # Fetch token from request headers
    token = current_user.token if hasattr(current_user, "token") else None
    if not token:
        raise HTTPException(status_code=401, detail="Authentication token missing")

    plan = create_quit_plan(user_id=current_user.id, token=token, db=db)
    
    if not plan:
        logger.warning("❌ No plan generated. User might not have completed the questionnaire.")
        raise HTTPException(status_code=400, detail="No plan generated.")

    return plan


@router.get("/get_plan/{user_id}")
def get_plan(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    logger.info(f"📢 Received request for User ID: {user_id}")

    plan = db.query(QuitPlan).filter(QuitPlan.user_id == user_id).first()
    if not plan:
        logger.warning(f"❌ No plan found for User ID: {user_id}")
        raise HTTPException(status_code=404, detail="Quit plan not found")

    logger.info(f"✅ Returning quit plan for User ID: {user_id}")
    return plan