from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from auth_services.routers.auth import router as auth_router
from auth_services.database import Base, engine

import logging

logging.basicConfig(level=logging.DEBUG)

# OAuth2 Security for Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

app = FastAPI(
    title="Auth Service",
    description="Handles user authentication and token generation",
    version="1.0",
    openapi_tags=[{"name": "Authentication", "description": "Operations related to user authentication"}]
)

# CORS Middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust as needed for your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Include authentication routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def root():
    return {"message": "Welcome to Auth Service!"}
