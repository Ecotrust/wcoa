from django.contrib import admin
from django.urls import include, path, re_path
from .views import create_wcoa_mapgroup, show_wcoa_planner, show_wcoa_embedded_map, search, show_wcoa_account_index, show_wcoa_mapgroups, show_wcoa_edit_mapgroups, show_wcoa_detail_mapgroups
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
    # Map Groups
    re_path(r'^collaborate/groups/create', create_wcoa_mapgroup, name='create_wcoa_mapgroup'),
    re_path(r'^collaborate/groups/$', show_wcoa_mapgroups, name='show_wcoa_mapgroups'),
    re_path(r'^groups/', show_wcoa_mapgroups, name='show_wcoa_mapgroups'),
    re_path(r'^collaborate/groups/(?P<pk>\d+)/(?P<slug>[\w-]+)/edit$', show_wcoa_edit_mapgroups, name='edit'),
    re_path(r'^groups/(?P<pk>\d+)/(?P<slug>[\w-]+)/edit$', show_wcoa_edit_mapgroups, name='edit'),
    re_path(r'^collaborate/groups/(?P<pk>\d+)/(?P<slug>[\w-]+)/$', show_wcoa_detail_mapgroups, name='detail'),
    # re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/join$',
    #     JoinMapGroupActionView.as_view(), name='join'),
    # re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/leave$',
    #     LeaveMapGroupActionView.as_view(), name='leave'),
    # re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/delete$',
    #     DeleteMapGroupActionView.as_view(), name='delete'),
    # re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/join$',
    #     RequestJoinMapGroupActionView.as_view(), name='request-join'),
    # re_path(r'^groups/create', create_wcoa_mapgroup, name='create_wcoa_mapgroup'),
    # re_path(r'^g/', RedirectView.as_view(url='/groups/')), # 301
    # re_path(r'^/$', views.index, name='index'),
]
