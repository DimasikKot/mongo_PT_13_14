from django.http import JsonResponse
from .mongo import pizzerias

def cheap_pizzas_report(request, price: int):
    pipeline = [
        {"$unwind": "$pizzas"},
        {"$match": {"pizzas.price": {"$lte": price}}},
        {"$project": {
            "_id": 0,
            "pizzeria": "$name",
            "pizza": "$pizzas.name",
            "price": "$pizzas.price"
        }}
    ]
    result = list(pizzerias.aggregate(pipeline))
    return JsonResponse(result, safe=False)

def expensive_pizzas_report(request, price: int):
    pipeline = [
        {"$unwind": "$pizzas"},
        {"$match": {"pizzas.price": {"$gte": price}}},
        {"$project": {
            "_id": 0,
            "pizzeria": "$name",
            "pizza": "$pizzas.name",
            "price": "$pizzas.price"
        }}
    ]
    result = list(pizzerias.aggregate(pipeline))
    return JsonResponse(result, safe=False)


def fast_recipes_report(request, time: int):
    pipeline = [
        {"$unwind": "$recipes"},
        {"$match": {"recipes.cooking_time_minutes": {"$lte": time}}},
        {"$project": {
            "_id": 0,
            "cookbook": "$cookbook_name",
            "recipe": "$recipes.title",
            "time": "$recipes.cooking_time_minutes"
        }}
    ]
    result = list(cookbooks.aggregate(pipeline))
    return JsonResponse(result, safe=False)

def low_ingredients_report(request, ingredients: int):
    try:
        pipeline = [
            {"$unwind": "$recipes"},
            {"$match": {"recipes.ingredients": {"$exists": True}}},
            {"$match": {"$expr": {"$lte": [{"$size": "$recipes.ingredients"}, ingredients]}}},
            {"$project": {
                "_id": 0,
                "cookbook": "$cookbook_name",
                "recipe": "$recipes.title",
                "ingredients": "$recipes.ingredients",
            }}
        ]
        
        result = list(cookbooks.aggregate(pipeline))
        return JsonResponse(result, safe=False)
        
    except ValueError:
        return JsonResponse({"error": "Неверный параметр ingredients. Оно должно быть числом."}, status=400)