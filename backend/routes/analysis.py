from fastapi import APIRouter, HTTPException

from services.supabase_client import supabase
from services.decision_engine import calculate_crop_survival_score
from services.recommendations_services import generate_recommendation


router = APIRouter(
    prefix="/analysis",
    tags=["AI Analysis"]
)


@router.post("/{case_id}")
def analyze_crop(case_id: str):

    # --------------------------------
    # 1. GET CROP CASE
    # --------------------------------

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

    crop_case = result.data[0]


    # --------------------------------
    # 2. GET CROP VALUES
    # --------------------------------

    health_score = float(
        crop_case.get("health_score") or 0
    )

    disease_severity = float(
        crop_case.get("disease_severity") or 0
    )

    recovery_probability = float(
        crop_case.get("recovery_probability") or 0
    )

    expected_revenue = float(
        crop_case.get("expected_revenue") or 0
    )

    money_invested = float(
        crop_case.get("money_invested") or 0
    )

    remaining_cost = float(
        crop_case.get("remaining_cost") or 0
    )


    # --------------------------------
    # 3. CALCULATE CROP SURVIVAL SCORE
    # --------------------------------

    score = calculate_crop_survival_score(
        health_score=health_score,
        disease_severity=disease_severity,
        recovery_probability=recovery_probability,
        expected_revenue=expected_revenue,
        money_invested=money_invested,
        remaining_cost=remaining_cost
    )


    # --------------------------------
    # 4. GENERATE RECOMMENDATION
    # --------------------------------

    recommendation_case = {
        "health_score": health_score,
        "disease_severity": disease_severity,
        "recovery_probability": recovery_probability,
        "expected_revenue": expected_revenue,
        "money_invested": money_invested,
        "remaining_cost": remaining_cost,

        # Optional treatment cost
        "treatment_cost": float(
            crop_case.get("treatment_cost") or 0
        )
    }

    recommendation = generate_recommendation(
        recommendation_case
    )


    # --------------------------------
    # 5. RETURN AI ANALYSIS
    # --------------------------------

    return {
        "success": True,
        "case_id": case_id,

        "crop_survival_score": score,

        "analysis": {
            "health_score": health_score,
            "disease_severity": disease_severity,
            "recovery_probability": recovery_probability
        },

        "recommendation": recommendation
    }