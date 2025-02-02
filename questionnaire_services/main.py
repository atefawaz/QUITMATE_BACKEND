from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from questionnaire_services.database import Base, engine
from questionnaire_services.routers import router as questionnaire_router

# Initialize FastAPI app
app = FastAPI()




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

# Create database tables
Base.metadata.create_all(bind=engine)

# Include questionnaire routes
app.include_router(questionnaire_router, prefix="/questionnaire", tags=["Questionnaire"])

@app.get("/")
def root():
    return {"message": "Welcome to the Questionnaire Service!"}
