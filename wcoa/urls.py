from django.contrib import admin
from django.urls import include, path, re_path
from .views import create_wcoa_mapgroup, show_wcoa_planner, show_wcoa_embedded_map, search, show_wcoa_account_index, show_wcoa_mapgroups

from . import views

app_name = 'wcoa'
handler404 = 'wcoa.views.page_not_found'
urlpatterns = [
    # path('', views.index, name='index'),
    re_path(r'^planner/$', show_wcoa_planner, name="planner_planner"),
    re_path(r'^visualize/$', show_wcoa_planner, name="planner"),
    re_path(r'^embed/map/$', show_wcoa_embedded_map, name="show_wcoa_embedded_map"),
    re_path(r'^search/', search, name='search'),
    re_path(r'^account/', show_wcoa_account_index, name="show_wcoa_account_index"),
    re_path(r'^collaborate/groups/create', create_wcoa_mapgroup, name='create_wcoa_mapgroup'),
    re_path(r'^collaborate/groups/', show_wcoa_mapgroups, name='show_wcoa_mapgroups'),
    re_path(r'^groups/', show_wcoa_mapgroups, name='show_wcoa_mapgroups'),
    # re_path(r'^groups/create', create_wcoa_mapgroup, name='create_wcoa_mapgroup'),
    # re_path(r'^g/', RedirectView.as_view(url='/groups/')), # 301
    # re_path(r'^/$', views.index, name='index'),
]
