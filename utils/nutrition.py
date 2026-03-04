import requests

def get_nutrition(food_name: str):
    """Fetch nutrition info from Open Food Facts API (free, no API key needed)"""

    url = "https://world.openfoodfacts.org/cgi/search.pl"

    params = {
        "search_terms": food_name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1
    }

    response = requests.get(url, params=params)
    result = response.json()

    if not result.get("products"):
        return {
            "calories": 0,
            "protein": 0,
            "carbs": 0
        }

    food = result["products"][0].get("nutriments", {})

    return {
        "calories": food.get("energy-kcal_100g", 0),
        "protein": food.get("proteins_100g", 0),
        "carbs": food.get("carbohydrates_100g", 0)
    }