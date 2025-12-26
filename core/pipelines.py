def cheap_pizzas_pipeline(price: int):
    return [
        {"$unwind": "$pizzas"},
        {"$match": {"pizzas.price": {"$lte": price}}},
        {"$project": {
            "_id": 0,
            "pizzeria": "$name",
            "pizza": "$pizzas.name",
            "price": "$pizzas.price"
        }}
    ]


def expensive_pizzas_pipeline(price: int):
    return [
        {"$unwind": "$pizzas"},
        {"$match": {"pizzas.price": {"$gte": price}}},
        {"$project": {
            "_id": 0,
            "pizzeria": "$name",
            "pizza": "$pizzas.name",
            "price": "$pizzas.price"
        }}
    ]


def fast_recipes_pipeline(time: int):
    return [
        {"$unwind": "$recipes"},
        {"$match": {"recipes.cooking_time_minutes": {"$lte": time}}},
        {"$project": {
            "_id": 0,
            "cookbook": "$cookbook_name",
            "recipe": "$recipes.title",
            "time": "$recipes.cooking_time_minutes"
        }}
    ]


def low_ingredients_pipeline(ingredients: int):
    return [
        {"$unwind": "$recipes"},
        {"$match": {
            "$expr": {
                "$lte": [
                    {"$size": "$recipes.ingredients"},
                    ingredients
                ]
            }
        }},
        {"$project": {
            "_id": 0,
            "cookbook": "$cookbook_name",
            "recipe": "$recipes.title",
            "ingredients": "$recipes.ingredients"
        }}
    ]
