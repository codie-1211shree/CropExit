from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from services.supabase_client import supabase


router = APIRouter(
    prefix="/crops",
    tags=["Crops"]
)


class CropCreate(BaseModel):
    farm_id: str
    crop_name: str
    variety: Optional[str] = None
    planting_date: Optional[str] = None
    growth_stage: Optional[str] = None
    area_acres: Optional[float] = None


class CropUpdate(BaseModel):
    crop_name: Optional[str] = None
    variety: Optional[str] = None
    planting_date: Optional[str] = None
    growth_stage: Optional[str] = None
    area_acres: Optional[float] = None


@router.post("/")
def create_crop(crop: CropCreate):

    # Check whether the farm exists
    farm = (
        supabase
        .table("farms")
        .select("id")
        .eq("id", crop.farm_id)
        .execute()
    )

    if not farm.data:
        raise HTTPException(
            status_code=404,
            detail="Farm not found"
        )

    response = (
        supabase
        .table("crops")
        .insert(crop.model_dump(exclude_none=True))
        .execute()
    )

    return {
        "success": True,
        "message": "Crop created successfully",
        "data": response.data
    }


@router.get("/")
def get_crops():

    response = (
        supabase
        .table("crops")
        .select("*")
        .execute()
    )

    return {
        "success": True,
        "data": response.data
    }


@router.get("/farm/{farm_id}")
def get_farm_crops(farm_id: str):

    response = (
        supabase
        .table("crops")
        .select("*")
        .eq("farm_id", farm_id)
        .execute()
    )

    return {
        "success": True,
        "data": response.data
    }


@router.get("/{crop_id}")
def get_crop(crop_id: str):

    response = (
        supabase
        .table("crops")
        .select("*")
        .eq("id", crop_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Crop not found"
        )

    return {
        "success": True,
        "data": response.data[0]
    }


@router.put("/{crop_id}")
def update_crop(crop_id: str, crop: CropUpdate):

    response = (
        supabase
        .table("crops")
        .update(crop.model_dump(exclude_none=True))
        .eq("id", crop_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Crop not found"
        )

    return {
        "success": True,
        "message": "Crop updated successfully",
        "data": response.data
    }


@router.delete("/{crop_id}")
def delete_crop(crop_id: str):

    response = (
        supabase
        .table("crops")
        .delete()
        .eq("id", crop_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=404,
            detail="Crop not found"
        )

    return {
        "success": True,
        "message": "Crop deleted successfully"
    }