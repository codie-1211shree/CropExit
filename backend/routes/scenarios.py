from fastapi import APIRouter, HTTPException
from services.supabase_client import supabase

router = APIRouter(
    prefix="/scenarios",
    tags=["Scenarios"]
)


@router.get("/{case_id}")
def get_scenarios(case_id: str):

    try:
        # Get crop case
        result = (
            supabase
            .table("crop_cases")
            .select("*")
            .eq("id", case_id)
            .single()
            .execute()
        )

        case = result.data

        if not case:
            raise HTTPException(
                status_code=404,
                detail="Crop case not found"
            )

        # -----------------------------
        # GET CROP DATA
        # -----------------------------

        health_score = float(case.get("health_score") or 0)
        disease_severity = float(case.get("disease_severity") or 0)
        money_invested = float(case.get("money_invested") or 0)
        treatment_cost = float(case.get("treatment_cost") or 0)
        remaining_cost = float(case.get("remaining_cost") or 0)
        expected_revenue = float(case.get("expected_revenue") or 0)
        recovery_probability = float(
            case.get("recovery_probability") or 0
        )

        # -----------------------------
        # SCENARIO 1: EXIT CROP
        # -----------------------------

        exit_loss = money_invested + treatment_cost

        exit_scenario = {
            "scenario": "EXIT_CROP",
            "description": "Stop further investment in the crop.",
            "additional_investment": 0,
            "expected_revenue": 0,
            "estimated_loss": round(exit_loss, 2),
            "risk_level": "LOW",
            "recommendation": "Exit the crop to prevent further losses."
        }

        # -----------------------------
        # SCENARIO 2: CONTINUE
        # -----------------------------

        continue_cost = remaining_cost

        continue_revenue = (
            expected_revenue *
            (recovery_probability / 100)
        )

        continue_profit = (
            continue_revenue - continue_cost
        )

        continue_scenario = {
            "scenario": "CONTINUE",
            "description": "Continue treatment with the current plan.",
            "additional_investment": round(continue_cost, 2),
            "expected_revenue": round(continue_revenue, 2),
            "projected_profit": round(continue_profit, 2),
            "risk_level": (
                "HIGH"
                if recovery_probability < 40
                else "MEDIUM"
                if recovery_probability < 70
                else "LOW"
            )
        }

        # -----------------------------
        # SCENARIO 3: INVEST MORE
        # -----------------------------

        extra_investment = treatment_cost * 1.5

        improved_recovery = min(
            recovery_probability + 20,
            95
        )

        improved_revenue = (
            expected_revenue *
            (improved_recovery / 100)
        )

        invest_profit = (
            improved_revenue
            - remaining_cost
            - extra_investment
        )

        invest_scenario = {
            "scenario": "INVEST_MORE",
            "description": "Invest additional money to improve recovery chances.",
            "additional_investment": round(extra_investment, 2),
            "expected_recovery_probability": round(
                improved_recovery, 2
            ),
            "expected_revenue": round(
                improved_revenue, 2
            ),
            "projected_profit": round(
                invest_profit, 2
            ),
            "risk_level": (
                "HIGH"
                if improved_recovery < 50
                else "MEDIUM"
                if improved_recovery < 75
                else "LOW"
            )
        }

        # -----------------------------
        # FIND BEST SCENARIO
        # -----------------------------

        scenario_profits = {
            "EXIT_CROP": float(-exit_loss),
            "CONTINUE": float(continue_profit),
            "INVEST_MORE": float(invest_profit)
        }

        best_scenario = "EXIT_CROP"
        best_profit = scenario_profits["EXIT_CROP"]

        if scenario_profits["CONTINUE"] > best_profit:
            best_scenario = "CONTINUE"
            best_profit = scenario_profits["CONTINUE"]

        if scenario_profits["INVEST_MORE"] > best_profit:
            best_scenario = "INVEST_MORE"
            best_profit = scenario_profits["INVEST_MORE"]

        # -----------------------------
        # FINAL RESPONSE
        # -----------------------------

        return {
            "success": True,
            "case_id": case_id,

            "current_crop_status": {
                "health_score": health_score,
                "disease_severity": disease_severity,
                "recovery_probability": recovery_probability
            },

            "scenarios": [
                exit_scenario,
                continue_scenario,
                invest_scenario
            ],

            "best_scenario": best_scenario,
            "best_projected_profit": round(best_profit, 2)
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )