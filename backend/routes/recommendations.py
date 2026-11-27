from fastapi import APIRouter, HTTPException
from services.supabase_client import supabase

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


def generate_recommendation(crop_case: dict) -> dict:

    health_score = float(crop_case.get("health_score") or 0)
    disease_severity = float(crop_case.get("disease_severity") or 0)
    recovery_probability = float(
        crop_case.get("recovery_probability") or 0
    )

    expected_revenue = float(
        crop_case.get("expected_revenue") or 0
    )

    treatment_cost = float(
        crop_case.get("treatment_cost") or 0
    )

    remaining_cost = float(
        crop_case.get("remaining_cost") or 0
    )

    future_cost = treatment_cost + remaining_cost

    if health_score < 30 or recovery_probability < 25:
        recommendation = "EXIT_CROP"
        reason = (
            "Crop health and recovery probability are very low. "
            "Further investment may increase the loss."
        )

    elif health_score < 50 or disease_severity >= 70:
        recommendation = "HARVEST_EARLY"
        reason = (
            "Crop condition is weak. Early harvesting can help "
            "reduce further losses."
        )

    elif health_score >= 60 and recovery_probability >= 60:
        recommendation = "CONTINUE"
        reason = (
            "Crop health and recovery probability are good. "
            "Continue cultivation and monitor the crop."
        )

    else:
        recommendation = "TREAT_AND_MONITOR"
        reason = (
            "The crop has moderate recovery potential. "
            "Apply treatment and monitor the crop closely."
        )

    projected_profit = expected_revenue - future_cost

    return {
        "recommendation": recommendation,
        "reason": reason,
        "health_score": health_score,
        "disease_severity": disease_severity,
        "recovery_probability": recovery_probability,
        "expected_revenue": expected_revenue,
        "future_cost": future_cost,
        "projected_profit": projected_profit
    }


@router.get("/{case_id}")
def get_recommendation(case_id: str):

    try:

        result = (
            supabase
            .table("crop_cases")
            .select("*")
            .eq("id", case_id)
            .single()
            .execute()
        )

        crop_case = result.data

        if not crop_case:
            raise HTTPException(
                status_code=404,
                detail="Crop case not found"
            )

        recommendation = generate_recommendation(crop_case)

        return {
            "success": True,
            "case_id": case_id,
            "data": recommendation
        }

    except HTTPException:
        raise

    except Exception as e:

        print("Recommendation error:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )