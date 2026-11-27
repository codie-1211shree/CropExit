from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.supabase_client import supabase

router = APIRouter(
    prefix="/farms",
    tags=["Farms"]
)


class FarmCreate(BaseModel):
    farm_name: str
    location: Optional[str] = None
    village: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    area_acres: Optional[float] = None
    soil_type: Optional[str] = None


class FarmUpdate(BaseModel):
    farm_name: Optional[str] = None
    location: Optional[str] = None
    village: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    area_acres: Optional[float] = None
    soil_type: Optional[str] = None


@router.post("/")
def create_farm(farm: FarmCreate):

    response = (
        supabase
        .table("farms")
        .insert(farm.model_dump(exclude_none=True))
        .execute()
    )

    return {
        "success": True,
        "message": "Farm created successfully",
        "data": response.data
    }


@router.get("/")
def get_farms():

    response = (
        supabase
        .table("farms")
        .select("*")
        .execute()
    )

    return {
        "success": True,
        "data": response.data
    }


@router.get("/{farm_id}")
def get_farm(farm_id: str):

    response = (
        supabase
        .table("farms")
        .select("*")
        .eq("id", farm_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Farm not found"
        )

    return {
        "success": True,
        "data": response.data[0]
    }


@router.put("/{farm_id}")
def update_farm(farm_id: str, farm: FarmUpdate):

    response = (
        supabase
        .table("farms")
        .update(farm.model_dump(exclude_none=True))
        .eq("id", farm_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Farm not found"
        )

    return {
        "success": True,
        "message": "Farm updated successfully",
        "data": response.data
    }


@router.delete("/{farm_id}")
def delete_farm(farm_id: str):

    response = (
        supabase
        .table("farms")
        .delete()
        .eq("id", farm_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Farm not found"
        )

    return {
        "success": True,
        "message": "Farm deleted successfully"
    }