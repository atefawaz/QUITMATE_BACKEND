from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth_services.database import get_db  # Updated import path
from auth_services.models import User  # Updated import path
from auth_services.schemas.user import UserCreate, UserResponse, Token, LoginRequest , RegisterResponse # Updated import path
from auth_services.services.auth import hash_password, verify_password, create_access_token  # Updated import path
from auth_services.schemas.user import Token
from auth_services.services.auth import verify_password, create_access_token , get_current_user 


router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    new_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        date_of_birth=user.date_of_birth,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT token
    token_data = {"sub": new_user.email, "user_id": new_user.id}
    access_token = create_access_token(data=token_data)

    # Redirect URL with token
    questionnaire_url = f"http://localhost:8001/questionnaire?token={access_token}"

    return {
        "id": new_user.id,
        "firstname": new_user.firstname,
        "lastname": new_user.lastname,
        "email": new_user.email,
        "date_of_birth": new_user.date_of_birth,
        "message": "User registered successfully. Please complete the questionnaire.",
        "redirect_url": questionnaire_url,
        "access_token": access_token,
        "token_type": "bearer"
    }




# @router.post("/login", response_model=Token)
# def login(user: LoginRequest, db: Session = Depends(get_db)):
#     """
#     Login endpoint that accepts JSON payload instead of form data.
#     """
#     db_user = db.query(User).filter(User.email == user.email).first()
    
#     if not db_user or not verify_password(user.password, db_user.password_hash):
#         raise HTTPException(status_code=400, detail="Invalid credentials")

#     token = create_access_token({"sub": db_user.email, "user_id": db_user.id})
    
#     return {"access_token": token, "token_type": "bearer"}


@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # user_block = get_current_user()
    # print(user_block)
    user_num_id = db_user.id

    token = create_access_token({"sub": db_user.email, "user_id": db_user.id})

    print(user_num_id)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_num_id": user_num_id  # ✅ Add user_id here
    }
