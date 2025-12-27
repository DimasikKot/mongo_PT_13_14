from django.urls import path
from . import views
from . import report_views

urlpatterns = [
    path("", views.index),

    path("pizzerias/", views.pizzerias_page),
    path("cookbooks/", views.cookbooks_page),

    path("pizzeria/add/", views.pizzeria_form),
    path("pizzeria/update/<str:id>/", views.pizzeria_form),
    path("pizzeria/delete/<str:id>/", views.delete_pizzeria_page),

    path("cookbook/add/", views.cookbook_form),
    path("cookbook/update/<str:id>/", views.cookbook_form),
    path("cookbook/delete/<str:id>/", views.delete_cookbook_page),

    path("reports/", report_views.reports_page),
    path('reports/pdf/', report_views.reports_pdf, name='reports_pdf'),
]
