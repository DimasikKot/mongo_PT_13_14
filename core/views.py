from django.shortcuts import render, redirect

from django.http import JsonResponse
from .mongo import pizzerias, cookbooks
from bson import ObjectId

import json

from .reports import *


def reports_page(request):
    result = None

    if "type" in request and "value" in request.GET:
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


def add_pizzeria_page(request):
    if request.method == "POST":
        pizzerias.insert_one({
            "name": request.POST["name"],
            "address": request.POST["address"],
            "phone": request.POST["phone"],
            "pizzas": []
        })
        return redirect("/pizzerias/")
    return render(request, "pizzeria_form.html", {"title": "Добавить пиццерию"})

def update_pizzeria_page(request, id):
    pizzeria = pizzerias.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        pizzerias.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "name": request.POST["name"],
                "address": request.POST["address"],
                "phone": request.POST["phone"]
            }}
        )
        return redirect("/pizzerias/")

    return render(
        request,
        "pizzeria_form.html",
        {
            "title": "Редактировать пиццерию",
            "pizzeria": pizzeria
        }
    )

def delete_pizzeria_page(request, id):
    pizzerias.delete_one({"_id": ObjectId(id)})
    return redirect("/pizzerias/")


def add_cookbook_page(request):
    if request.method == "POST":
        cookbooks.insert_one({
            "cookbook_name": request.POST["cookbook_name"],
            "recipes": []
        })
        return redirect("/cookbooks/")

    return render(
        request,
        "cookbook_form.html",
        {"title": "Добавить кулинарную книгу"}
    )

def update_cookbook_page(request, id):
    cookbook = cookbooks.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        cookbooks.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "cookbook_name": request.POST["cookbook_name"]
            }}
        )
        return redirect("/cookbooks/")

    return render(
        request,
        "cookbook_form.html",
        {
            "title": "Редактировать кулинарную книгу",
            "cookbook": cookbook
        }
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
