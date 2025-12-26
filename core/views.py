from django.shortcuts import render

from django.http import JsonResponse
from .mongo import pizzerias, cookbooks
from bson import ObjectId

import json


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
