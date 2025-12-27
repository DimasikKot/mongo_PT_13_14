def _join_array(field: str) -> dict:
    """Вспомогательная функция для соединения массива в строку через запятую"""
    return {
        "$reduce": {
            "input": field,
            "initialValue": "",
            "in": {
                "$cond": [
                    {"$eq": ["$$value", ""]},
                    "$$this",
                    {"$concat": ["$$value", ", ", "$$this"]}
                ]
            }
        }
    }


def cheap_pizzas_pipeline(price: int):
    return [
        {"$unwind": "$pizzas"},
        {"$match": {"pizzas.price": {"$lte": price}}},
        {"$project": {
            "_id": 0,
            "Пиццерия": "$name",
            "Пицца": "$pizzas.name",
            "Цена ₽": "$pizzas.price",
            "Вес (г)": "$pizzas.weight",
            "Ингредиенты": {
                "$cond": {
                    "if": {"$isArray": "$pizzas.ingredients"},
                    "then": _join_array("$pizzas.ingredients"),
                    "else": ""
                }
            }
        }},
        {"$sort": {"Цена ₽": 1}}
    ]


def expensive_pizzas_pipeline(price: int):
    return [
        {"$unwind": "$pizzas"},
        {"$match": {"pizzas.price": {"$gte": price}}},
        {"$project": {
            "_id": 0,
            "Пиццерия": "$name",
            "Пицца": "$pizzas.name",
            "Цена ₽": "$pizzas.price",
            "Вес (г)": "$pizzas.weight",
            "Ингредиенты": {
                "$cond": {
                    "if": {"$isArray": "$pizzas.ingredients"},
                    "then": _join_array("$pizzas.ingredients"),
                    "else": ""
                }
            }
        }},
        {"$sort": {"Цена ₽": -1}}
    ]


def fast_recipes_pipeline(time: int):
    return [
        {"$unwind": "$recipes"},
        {"$match": {"recipes.cooking_time_minutes": {"$lte": time}}},
        {"$project": {
            "_id": 0,
            "Кулинарная книга": "$cookbook_name",
            "Рецепт": "$recipes.title",
            "Время (мин)": "$recipes.cooking_time_minutes",
            "Ингредиенты": {
                "$cond": {
                    "if": {"$isArray": "$recipes.ingredients"},
                    "then": _join_array("$recipes.ingredients"),
                    "else": ""
                }
            }
        }},
        {"$sort": {"Время (мин)": 1}}
    ]


def low_ingredients_pipeline(ingredients: int):
    return [
        {"$unwind": "$recipes"},
        {"$addFields": {
            "ing_count": {"$size": {"$ifNull": ["$recipes.ingredients", []]}}
        }},
        {"$match": {"ing_count": {"$lte": ingredients}}},
        {"$project": {
            "_id": 0,
            "Кулинарная книга": "$cookbook_name",
            "Рецепт": "$recipes.title",
            "Кол-во ингредиентов": "$ing_count",
            "Ингредиенты": {
                "$cond": {
                    "if": {"$isArray": "$recipes.ingredients"},
                    "then": _join_array("$recipes.ingredients"),
                    "else": ""
                }
            }
        }},
        {"$sort": {"Кол-во ингредиентов": 1}}
    ]