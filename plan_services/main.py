from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import plan_routes
import logging


app = FastAPI()


# ✅ Create a logger instance
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ✅ Allow requests from frontend (React at localhost:3000)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ✅ Allow specific frontend origins
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # ✅ Allow all headers
)


Base.metadata.create_all(bind=engine)

# Include API routes
app.include_router(plan_routes.router, prefix="/plan", tags=["Quitting Plan"])

@app.get("/")
def root():
    """Root endpoint to check if service is running"""
    return {"message": "Welcome to the Quitting Plan Service!"}
