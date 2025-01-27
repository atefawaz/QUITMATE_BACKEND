from fastapi import FastAPI
from questionnaire_services.database import Base, engine
from questionnaire_services.routers import router as questionnaire_router

app = FastAPI(
    title="Questionnaire Service",
    description="Service for managing questionnaires.",
    version="1.0.0",
)

# Include the questionnaire router
app.include_router(questionnaire_router)

# Create tables for this service
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
