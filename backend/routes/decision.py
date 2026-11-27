from fastapi import APIRouter, HTTPException
from services.supabase_client import supabase
from services.decision_engine import calculate_crop_survival_score
from services.decision_engine import get_recommendation

router = APIRouter(
    prefix="/decision",
    tags=["Final Decision"]
)


@router.get("/{case_id}")
def get_final_decision(case_id: str):

    # 1. Get crop case
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

    case = result.data[0]

    # 2. Get crop
    crop_result = (
        supabase
        .table("crops")
        .select("*")
        .eq("id", case["crop_id"])
        .execute()
    )

    if not crop_result.data:
        raise HTTPException(
            status_code=404,
            detail="Crop not found"
        )

    crop = crop_result.data[0]

    # 3. Current MVP risk values
    # These will later come from real APIs/models.
    weather_risk = 20
    market_risk = 25

    # 4. Get values from crop case
    health_score = case.get("health_score") or 0
    disease_severity = case.get("disease_severity") or 0
    recovery_probability = case.get("recovery_probability") or 0

    expected_revenue = case.get("expected_revenue") or 0
    money_invested = case.get("money_invested") or 0
    remaining_cost = case.get("remaining_cost") or 0

    # 5. Calculate survival score
    survival_score = calculate_crop_survival_score(
        health_score=health_score,
        disease_severity=disease_severity,
        recovery_probability=recovery_probability,
        expected_revenue=expected_revenue,
        money_invested=money_invested,
        remaining_cost=remaining_cost,
        weather_risk=weather_risk,
        market_risk=market_risk
    )

    # 6. Final recommendation
    recommendation = get_recommendation(
        survival_score
    )

    return {
        "success": True,
        "case_id": case_id,
        "crop": crop.get("crop_name"),
        "survival_score": survival_score,
        "recommendation": recommendation,
        "risk_factors": {
            "weather_risk": weather_risk,
            "market_risk": market_risk
        },
        "financial": {
            "money_invested": money_invested,
            "remaining_cost": remaining_cost,
            "expected_revenue": expected_revenue
        }
    }