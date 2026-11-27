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
        reason = "Crop health and recovery probability are very low."

    elif health_score < 50 or disease_severity >= 70:
        recommendation = "HARVEST_EARLY"
        reason = "Crop condition is weak. Early harvesting can reduce further losses."

    elif recovery_probability >= 60 and health_score >= 60:
        recommendation = "CONTINUE"
        reason = "Crop health and recovery probability are good."

    else:
        recommendation = "TREAT_AND_MONITOR"
        reason = "Moderate crop condition. Treat the crop and monitor it closely."

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