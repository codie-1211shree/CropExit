from fastapi import APIRouter, HTTPException
from services.supabase_client import supabase

router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)


@router.get("/{farm_id}")
def get_weather(farm_id: str):

    # Get farm information
    result = (
        supabase
        .table("farms")
        .select("*")
        .eq("id", farm_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=404,
            detail="Farm not found"
        )

    farm = result.data[0]

    # Temporary weather data for MVP testing
    # Later we will replace this with a real weather API.
    weather = {
        "temperature": 31,
        "humidity": 72,
        "rainfall_mm": 12,
        "wind_speed": 14,
        "condition": "Partly Cloudy"
    }

    return {
        "success": True,
        "farm_id": farm_id,
        "location": farm.get("location"),
        "weather": weather
    }