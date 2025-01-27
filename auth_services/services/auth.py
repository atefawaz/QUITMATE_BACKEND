from bcrypt import hashpw, gensalt, checkpw
from jose import jwt
from datetime import datetime, timedelta
from auth_services.config import settings  # Updated import for settings

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
