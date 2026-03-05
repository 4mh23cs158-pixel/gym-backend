import requests

def search_food(query: str):
    """Search for food items from Open Food Facts API"""
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": query,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 10
    }
    try:
        response = requests.get(url, params=params)
        result = response.json()
        
        products = []
        for p in result.get("products", []):
            products.append({
                "id": p.get("_id") or p.get("id"),
                "name": p.get("product_name") or "Unknown Product",
                "brand": p.get("brands", ""),
                "image": p.get("image_front_small_url", ""),
                "serving_size": p.get("serving_size", "")
            })
        return products
    except Exception as e:
        print(f"Search error: {e}")
        return []

def get_nutrition(food_name: str, quantity: float = 100, unit: str = "grams"):
    """Fetch and calculate nutrition info based on quantity and unit"""

    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": food_name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1
    }

    try:
        response = requests.get(url, params=params)
        result = response.json()
    except Exception:
        return {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}

    if not result.get("products"):
        return {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}

    product = result["products"][0]
    nutriments = product.get("nutriments", {})

    # Base values per 100g
    base_cal = nutriments.get("energy-kcal_100g", 0)
    base_pro = nutriments.get("proteins_100g", 0)
    base_carbs = nutriments.get("carbohydrates_100g", 0)
    base_fat = nutriments.get("fat_100g", 0)

    # Conversion factor to grams
    multiplier = 1.0
    if unit == "cups":
        multiplier = 240.0 # Approximate
    elif unit == "servings":
        # Try to find serving size in grams
        serving_g = product.get("serving_quantity")
        if not serving_g:
            # Try parsing from serving_size string (e.g., "100 g")
            ss_str = product.get("serving_size", "")
            if "g" in ss_str.lower():
                try:
                    serving_g = float(ss_str.lower().split("g")[0].strip())
                except:
                    serving_g = 100.0
            else:
                serving_g = 100.0
        multiplier = float(serving_g)

    # Final calculation: (base / 100) * (quantity * multiplier)
    total_grams = quantity * multiplier
    ratio = total_grams / 100.0

    return {
        "calories": round(base_cal * ratio, 1),
        "protein": round(base_pro * ratio, 1),
        "carbs": round(base_carbs * ratio, 1),
        "fat": round(base_fat * ratio, 1)
    }