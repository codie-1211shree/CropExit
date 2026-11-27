from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.crop_cases import router as crop_cases_router
from routes.farms import router as farms_router
from routes.crops import router as crops_router
from routes.analysis import router as analysis_router
from routes.weather import router as weather_router
from routes.market import router as market_router
from routes.decision import router as decision_router
from services.supabase_client import supabase
from routes.recommendations import router as recommendations_router
from routes.scenarios import router as scenarios_router

app = FastAPI(
    title="CropExit AI API",
    description="AI-powered crop loss prevention and decision-support system",
    version="1.0.0"
)
app.include_router(recommendations_router)
app.include_router(weather_router)
app.include_router(market_router)
app.include_router(farms_router)
app.include_router(crops_router)
app.include_router(crop_cases_router)
app.include_router(analysis_router)
app.include_router(decision_router)
app.include_router(scenarios_router)

@app.get("/")
def root():
    return {
        "message": "CropExit AI Backend is running 🌱",
        "status": "success"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }