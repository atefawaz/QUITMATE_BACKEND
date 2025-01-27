from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth_services.database import get_db  # Updated import path
from auth_services.models import User  # Updated import path
from auth_services.schemas.user import UserCreate, UserResponse, Token, LoginRequest  # Updated import path
from auth_services.services.auth import hash_password, verify_password, create_access_token  # Updated import path

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to register a new user.

    Args:
        user (UserCreate): The user details provided in the request body.
        db (Session): The database session dependency.

    Returns:
        UserResponse: The registered user's details (excluding password).
    """
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
        password_hash=hashed_password  # Updated field name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(user: LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint to log in a user.

    Args:
        user (LoginRequest): The login credentials provided in the request body.
        db (Session): The database session dependency.

    Returns:
        Token: The access token for the authenticated user.
    """
    # Check if the user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):  # Updated field name
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # Generate a token
    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}
