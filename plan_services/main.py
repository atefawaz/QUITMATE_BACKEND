import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import plan_routes

app = FastAPI()

# ✅ Fix: Initialize logger properly
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
# ✅ Create tables in the database
Base.metadata.create_all(bind=engine)

# ✅ Include API routes
app.include_router(plan_routes.router, prefix="/plan", tags=["Quitting Plan"])

@app.get("/")
def root():
    """Root endpoint to check if the service is running"""
    return {"message": "Welcome to the Quitting Plan Service!"}