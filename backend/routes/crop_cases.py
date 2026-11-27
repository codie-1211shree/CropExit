from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.supabase_client import supabase

router = APIRouter(prefix="/crop-cases", tags=["Crop Cases"])


class CropCaseCreate(BaseModel):
    crop_id: str
    money_invested: float = 0
    treatment_cost: float = 0
    remaining_cost: float = 0
    expected_yield: Optional[float] = None
    market_price: Optional[float] = None
    expected_revenue: Optional[float] = None
    recovery_probability: Optional[float] = None
    health_score: Optional[float] = None
    disease_severity: Optional[float] = None
    status: str = "active"


@router.post("/")
def create_crop_case(case: CropCaseCreate):

    result = (
        supabase
        .table("crop_cases")
        .insert(case.model_dump())
        .execute()
    )

    return {
        "success": True,
        "message": "Crop case created successfully",
        "data": result.data
    }


@router.get("/")
def get_crop_cases():

    result = (
        supabase
        .table("crop_cases")
        .select("*")
        .execute()
    )

    return {
        "success": True,
        "data": result.data
    }


@router.get("/{case_id}")
def get_crop_case(case_id: str):

    result = (
        supabase
        .table("crop_cases")
        .select("*")
        .eq("id", case_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(
            status_code=404,
            detail="Crop case not found"
        )

    return {
        "success": True,
        "data": result.data[0]
    }