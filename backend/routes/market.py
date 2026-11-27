from fastapi import APIRouter

router = APIRouter(
    prefix="/market",
    tags=["Market"]
)


# Temporary MVP market-price data
MARKET_PRICES = {
    "Tomato": {
        "price_per_kg": 28,
        "market": "APMC Vashi",
        "unit": "₹/kg"
    },
    "Onion": {
        "price_per_kg": 32,
        "market": "APMC Vashi",
        "unit": "₹/kg"
    },
    "Potato": {
        "price_per_kg": 25,
        "market": "APMC Vashi",
        "unit": "₹/kg"
    },
    "Wheat": {
        "price_per_kg": 30,
        "market": "APMC Vashi",
        "unit": "₹/kg"
    }
}


@router.get("/{crop_name}")
def get_market_price(crop_name: str):

    crop = crop_name.strip().title()

    data = MARKET_PRICES.get(crop)

    if not data:
        return {
            "success": False,
            "message": "Market price not available for this crop",
            "crop_name": crop
        }

    return {
        "success": True,
        "crop_name": crop,
        "data": data
    }