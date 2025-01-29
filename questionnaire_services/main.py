from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from questionnaire_services.database import Base, engine
from questionnaire_services.routers import router as questionnaire_router

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include questionnaire routes
app.include_router(questionnaire_router, prefix="/questionnaire", tags=["Questionnaire"])

@app.get("/")
def root():
    return {"message": "Welcome to the Questionnaire Service!"}
