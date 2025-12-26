from django.shortcuts import render, redirect

from django.http import JsonResponse
from .mongo import pizzerias, cookbooks
from bson import ObjectId

import json

from .reports import *


def reports_page(request):
    result = None

    if "type" in request.GET and "value" in request.GET:
        t = request.GET["type"]
        v = int(request.GET["value"])

        if t == "cheap":
            result = list(pizzerias.aggregate(cheap_pizzas_pipeline(v)))
        elif t == "expensive":
            result = list(pizzerias.aggregate(expensive_pizzas_pipeline(v)))
        elif t == "fast":
            result = list(cookbooks.aggregate(fast_recipes_pipeline(v)))
        elif t == "low":
            result = list(cookbooks.aggregate(low_ingredients_pipeline(v)))

    return render(request, "reports.html", {"result": result})


def index(request):
    return render(request, "index.html")


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


def add_pizzeria(request):
    if request.method == "POST":
        body = json.loads(request.body)
        pizzerias.insert_one(body)
        return JsonResponse({"status": "added"})

def add_cookbook(request):
    if request.method == "POST":
        body = json.loads(request.body)
        cookbooks.insert_one(body)
        return JsonResponse({"status": "added"})


def get_pizzerias(request):
    data = list(pizzerias.find({}, {"_id": 0}))
    return JsonResponse(data, safe=False)

def get_cookbooks(request):
    data = list(cookbooks.find({}, {"_id": 0}))
    return JsonResponse(data, safe=False)


def update_pizzeria(request, id):
    if request.method == "POST":
        body = json.loads(request.body)
        pizzerias.update_one({"_id": ObjectId(id)}, {"$set": body})
        return JsonResponse({"status": "updated"})

def update_cookbook(request, id):
    if request.method == "POST":
        body = json.loads(request.body)
        cookbooks.update_one({"_id": ObjectId(id)}, {"$set": body})
        return JsonResponse({"status": "updated"})


def delete_pizzeria(request, id):
    pizzerias.delete_one({"_id": ObjectId(id)})
    return JsonResponse({"status": "deleted"})

def delete_cookbook(request, id):
    cookbooks.delete_one({"_id": ObjectId(id)})
    return JsonResponse({"status": "deleted"})
