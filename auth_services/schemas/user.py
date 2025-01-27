from pydantic import BaseModel, EmailStr, Field
from datetime import date

# Schema for creating a new user
class UserCreate(BaseModel):
    firstname: str = Field(..., min_length=2, max_length=50)
    lastname: str = Field(..., min_length=2, max_length=50)
    date_of_birth: date
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str

# Schema for user response (excluding sensitive fields like password)
class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    date_of_birth: date

    class Config:
        orm_mode = True

# Schema for login request
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

# Schema for token response
class Token(BaseModel):
    access_token: str
    token_type: str
