from django.http import JsonResponse
from .mongo import pizzerias, cookbooks
from .pipelines import *

def cheap_pizzas_report(request, price: int):
    result = list(pizzerias.aggregate(cheap_pizzas_pipeline(price)))
    return JsonResponse(result, safe=False)


def expensive_pizzas_report(request, price: int):
    result = list(pizzerias.aggregate(expensive_pizzas_pipeline(price)))
    return JsonResponse(result, safe=False)


def fast_recipes_report(request, time: int):
    result = list(cookbooks.aggregate(fast_recipes_pipeline(time)))
    return JsonResponse(result, safe=False)


def low_ingredients_report(request, ingredients: int):
    result = list(cookbooks.aggregate(low_ingredients_pipeline(ingredients)))
    return JsonResponse(result, safe=False)
