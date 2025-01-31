import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import plan_routes

app = FastAPI()

# ✅ Fix: Initialize logger properly
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Fix CORS: Allow frontend access
origins = [
    "http://localhost:3000",  # Frontend URL
    "http://127.0.0.1:3000"   # Alternative localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# ✅ Create tables in the database
Base.metadata.create_all(bind=engine)

# ✅ Include API routes
app.include_router(plan_routes.router, prefix="/plan", tags=["Quitting Plan"])

@app.get("/")
def root():
    """Root endpoint to check if the service is running"""
    return {"message": "Welcome to the Quitting Plan Service!"}