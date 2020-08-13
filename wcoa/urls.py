from django.contrib import admin
from django.urls import include, path, re_path
from .views import show_wcoa_planner, show_wcoa_embedded_map, search

from . import views

app_name = 'wcoa'
handler404 = 'wcoa.views.page_not_found'
urlpatterns = [
    # path('', views.index, name='index'),
    re_path(r'^planner/$', show_wcoa_planner, name="planner_planner"),
    re_path(r'^visualize/$', show_wcoa_planner, name="planner"),
    re_path(r'^embed/map/$', show_wcoa_embedded_map, name="show_wcoa_embedded_map"),
    re_path(r'^search/', search, name='search'),
    # re_path(r'^/$', views.index, name='index'),
]
