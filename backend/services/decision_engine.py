def calculate_crop_survival_score(
    health_score,
    disease_severity,
    recovery_probability,
    expected_revenue,
    money_invested,
    remaining_cost,
    weather_risk=0,
    market_risk=0
):
    # Convert database values to numbers
    health_score = float(health_score or 0)
    disease_severity = float(disease_severity or 0)
    recovery_probability = float(recovery_probability or 0)
    expected_revenue = float(expected_revenue or 0)
    money_invested = float(money_invested or 0)
    remaining_cost = float(remaining_cost or 0)
    weather_risk = float(weather_risk or 0)
    market_risk = float(market_risk or 0)

    # Health component
    health_component = health_score * 0.25

    # Disease component
    disease_component = (100 - disease_severity) * 0.20

    # Recovery component
    recovery_component = recovery_probability * 0.20

    # Financial component
    total_investment = money_invested + remaining_cost

    if total_investment > 0:
        financial_ratio = (
            expected_revenue / total_investment
        ) * 100
    else:
        financial_ratio = 100

    financial_ratio = min(financial_ratio, 100)

    financial_component = financial_ratio * 0.20

    # Weather + market risk
    risk_component = (
        (100 - weather_risk) * 0.075
        + (100 - market_risk) * 0.075
    )

    score = (
        health_component
        + disease_component
        + recovery_component
        + financial_component
        + risk_component
    )

    return round(min(max(score, 0), 100), 2)


def get_recommendation(score):

    if score <= 30:
        return "EXIT"

    elif score <= 50:
        return "HARVEST_EARLY"

    elif score <= 70:
        return "TREAT"

    else:
        return "CONTINUE"