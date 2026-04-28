from fastapi import APIRouter


router = APIRouter(prefix="/v1", tags=["purpose taxonomy"])


@router.get("/purpose-taxonomy")
async def get_purpose_taxonomy() -> dict:
    return {
        "launch_use_cases": [
            {
                "label": "Buy or rent a home",
                "purpose_category": "live_relocate",
                "sub_purpose": "buy_or_rent_home",
            },
            {
                "label": "Cafe / restaurant / cloud kitchen",
                "purpose_category": "retail_food_local_service",
                "sub_purpose": "food_and_beverage",
            },
            {
                "label": "Sports facility",
                "purpose_category": "fitness_sports_site",
                "sub_purpose": "sports_facility",
            },
            {
                "label": "Gym / fitness studio",
                "purpose_category": "fitness_sports_site",
                "sub_purpose": "gym_fitness_studio",
            },
            {
                "label": "Franchise / storefront",
                "purpose_category": "retail_food_local_service",
                "sub_purpose": "franchise_storefront",
            },
        ],
        "free_text_supported": True,
    }

