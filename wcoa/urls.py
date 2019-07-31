from django.contrib import admin
from django.urls import include, path, re_path
from .views import show_wcoa_planner

from . import views

app_name = 'wcoa'
urlpatterns = [
    # path('', views.index, name='index'),
    path('/', views.index, name='index'),
    re_path(r'^planner/', show_wcoa_planner, name="planner_planner"),
    re_path(r'^visualize/', show_wcoa_planner, name="planner"),
]
