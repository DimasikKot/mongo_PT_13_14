from django.shortcuts import render, redirect

from django.http import JsonResponse
from .mongo import pizzerias, cookbooks
from bson import ObjectId

import json


def index(request):
    # Количество пиццерий
    pizzerias_count = pizzerias.count_documents({})

    # Общее количество пицц через агрегацию
    pizza_agg = pizzerias.aggregate([
        {"$project": {"count": {"$size": {"$ifNull": ["$pizzas", []]}}}},
        {"$group": {"_id": None, "total": {"$sum": "$count"}}}
    ])
    pizza_result = next(pizza_agg, {"total": 0})
    total_pizzas = pizza_result["total"]

    # Количество кулинарных книг
    cookbooks_count = cookbooks.count_documents({})

    # Общее количество рецептов через агрегацию
    recipe_agg = cookbooks.aggregate([
        {"$project": {"count": {"$size": {"$ifNull": ["$recipes", []]}}}},
        {"$group": {"_id": None, "total": {"$sum": "$count"}}}
    ])
    recipe_result = next(recipe_agg, {"total": 0})
    total_recipes = recipe_result["total"]

    return render(request, "index.html", {
        "pizzerias_count": pizzerias_count,
        "total_pizzas": total_pizzas,
        "cookbooks_count": cookbooks_count,
        "total_recipes": total_recipes,
    })


def pizzerias_page(request):
    data = list(pizzerias.find())
    for p in data:
        p["id"] = str(p["_id"])
    return render(request, "pizzerias.html", {"pizzerias": data})

def cookbooks_page(request):
    data = list(cookbooks.find())
    for c in data:
        c["id"] = str(c["_id"])
    return render(request, "cookbooks.html", {"cookbooks": data})


def pizzeria_form(request, id=None):
    pizzeria = None

    if id:
        pizzeria = pizzerias.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        pizzas = []

        pizza_names = request.POST.getlist("pizza_name")
        pizza_prices = request.POST.getlist("pizza_price")
        pizza_weights = request.POST.getlist("pizza_weight")
        pizza_ingredients = request.POST.getlist("pizza_ingredients")

        for i in range(len(pizza_names)):
            if not pizza_names[i].strip():
                continue
            if not pizza_prices[i].isdigit() or not pizza_weights[i].isdigit():
                continue

            pizzas.append({
                "name": pizza_names[i],
                "price": int(pizza_prices[i]),
                "weight": int(pizza_weights[i]),
                "ingredients": [
                    ing.strip()
                    for ing in pizza_ingredients[i].split(",")
                    if ing.strip()
                ]
            })

        data = {
            "name": request.POST["name"],
            "address": request.POST["address"],
            "phone": request.POST["phone"],
            "pizzas": pizzas
        }

        if id:
            pizzerias.update_one(
                {"_id": ObjectId(id)},
                {"$set": data}
            )
        else:
            pizzerias.insert_one(data)

        return redirect("/pizzerias/")

    return render(
        request,
        "pizzeria_form.html",
        {"pizzeria": pizzeria}
    )

def delete_pizzeria_page(request, id):
    pizzerias.delete_one({"_id": ObjectId(id)})
    return redirect("/pizzerias/")


def cookbook_form(request, id=None):
    cookbook = None

    if id:
        cookbook = cookbooks.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        recipes = []

        titles = request.POST.getlist("recipe_title")
        times = request.POST.getlist("recipe_time")
        ingredients = request.POST.getlist("recipe_ingredients")

        for i in range(len(titles)):
            if not titles[i].strip():
                continue
            if not times[i].isdigit():
                continue

            recipes.append({
                "title": titles[i],
                "cooking_time_minutes": int(times[i]),
                "ingredients": [
                    ing.strip()
                    for ing in ingredients[i].split(",")
                    if ing.strip()
                ]
            })

        data = {
            "cookbook_name": request.POST["cookbook_name"],
            "recipes": recipes
        }

        if id:
            cookbooks.update_one(
                {"_id": ObjectId(id)},
                {"$set": data}
            )
        else:
            cookbooks.insert_one(data)

        return redirect("/cookbooks/")

    return render(
        request,
        "cookbook_form.html",
        {"cookbook": cookbook}
    )

def delete_cookbook_page(request, id):
    cookbooks.delete_one({"_id": ObjectId(id)})
    return redirect("/cookbooks/")
