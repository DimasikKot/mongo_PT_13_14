from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),

    path("pizzerias/", views.pizzerias_page),
    path("cookbooks/", views.cookbooks_page),

    path("pizzeria/add/", views.add_pizzeria_page),
    path("pizzeria/update/<str:id>/", views.update_pizzeria_page),
    path("pizzeria/delete/<str:id>/", views.delete_pizzeria_page),

    path("cookbook/add/", views.add_cookbook_page),
    path("cookbook/update/<str:id>/", views.update_cookbook_page),
    path("cookbook/delete/<str:id>/", views.delete_cookbook_page),

    path("reports/", views.reports_page),
]
