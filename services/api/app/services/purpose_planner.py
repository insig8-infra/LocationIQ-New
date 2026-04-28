from app.models import PurposeSummary


def infer_purpose(use_case_input: str) -> PurposeSummary:
    normalized = use_case_input.lower()

    if any(term in normalized for term in ["pickleball", "turf", "badminton", "sport"]):
        return PurposeSummary(
            purpose_category="fitness_sports_site",
            sub_purpose="pickleball_facility" if "pickleball" in normalized else "sports_facility",
            display_label="Pickleball facility" if "pickleball" in normalized else "Sports facility",
        )

    if any(term in normalized for term in ["gym", "fitness", "yoga", "pilates"]):
        return PurposeSummary(
            purpose_category="fitness_sports_site",
            sub_purpose="gym_fitness_studio",
            display_label="Gym / fitness studio",
        )

    if any(term in normalized for term in ["cafe", "restaurant", "cloud kitchen", "qsr", "bakery"]):
        return PurposeSummary(
            purpose_category="retail_food_local_service",
            sub_purpose="food_and_beverage",
            display_label="Cafe / restaurant / cloud kitchen",
        )

    if any(term in normalized for term in ["home", "3bhk", "rent", "buy", "relocate", "pg"]):
        return PurposeSummary(
            purpose_category="live_relocate",
            sub_purpose="buy_or_rent_home",
            display_label="Buy or rent a home",
        )

    if any(term in normalized for term in ["franchise", "store", "shop", "salon", "pharmacy"]):
        return PurposeSummary(
            purpose_category="retail_food_local_service",
            sub_purpose="franchise_storefront",
            display_label="Franchise / storefront",
        )

    return PurposeSummary(
        purpose_category="general_location_read",
        sub_purpose="custom_use_case",
        display_label=use_case_input.strip()[:80],
    )

