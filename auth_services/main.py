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

origins = [
    "http://localhost:8081",  # Your frontend in Expo
    "http://127.0.0.1:8081",
    "http://localhost:3000",  # If running on port 3000
    "http://127.0.0.1:3000",
    "http://localhost:8082",  # React Native Web on Mac
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow only specific frontend origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# ✅ Enable CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific frontend origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Include authentication routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def root():
    return {"message": "Welcome to Auth Service!"}
