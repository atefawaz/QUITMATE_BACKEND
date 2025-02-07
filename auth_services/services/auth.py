from bcrypt import hashpw, gensalt, checkpw
from jose import jwt, JWTError
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth_services.config import settings
from auth_services.database import get_db
from auth_services.models import User

# OAuth2 scheme for extracting the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Hash password
def hash_password(password: str) -> str:
    """
    Hashes a plain text password using bcrypt.

    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """
    return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that a plain text password matches its hashed version.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if passwords match, False otherwise.
    """
    return checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

# Create JWT token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=settings.access_token_expire_minutes)) -> str:
    """
    Creates a JWT token with expiration.

    Args:
        data (dict): Data to include in the token payload.
        expires_delta (timedelta): Token expiration duration.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


# def get_current_user(
#     token: str = Depends(oauth2_scheme), 
#     db: Session = Depends(get_db)
# ) -> User:
#     """
#     Decodes the JWT token and retrieves the authenticated user.

#     Args:
#         token (str): JWT access token.
#         db (Session): Database session.

#     Returns:
#         User: Authenticated user object with token.
#     """
#     try:
#         payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
#         user_id: int = payload.get("user_id")
#         if user_id is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")

#     user = db.query(User).filter(User.id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
#     # ✅ Attach token to user object for further requests
#     setattr(user, "token", token)

#     return { user , user_id}


# def get_current_user(
#     token: str = Depends(oauth2_scheme), 
#     db: Session = Depends(get_db)
# ) -> User:
#     try:
#         payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
#         user_id: int = payload.get("user_id")
#         if user_id is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")

#     user = db.query(User).filter(User.id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     return user  



def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> User:
    """
    Decodes the JWT token and retrieves the authenticated user.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # ✅ Attach token to user object
    setattr(user, "token", token)

    return user  # ✅ Return only the user object, not a set