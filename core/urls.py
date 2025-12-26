from django.urls import path
from . import views

urlpatterns = [
    path("pizzeria/add/", views.add_pizzeria),
    path("cookbook/add/", views.add_cookbook),
    path("pizzerias/", views.get_pizzerias),
    path("cookbooks/", views.get_cookbooks),
    path("pizzeria/update/<str:id>/", views.update_pizzeria),
    path("cookbook/update/<str:id>/", views.update_cookbook),
    path("pizzeria/delete/<str:id>/", views.delete_pizzeria),
    path("cookbook/delete/<str:id>/", views.delete_cookbook),
]
