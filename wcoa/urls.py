from django.contrib import admin
from django.urls import include, path, re_path
from .views import create_wcoa_mapgroup, show_wcoa_planner, show_wcoa_embedded_map, search, show_wcoa_account_index, show_wcoa_mapgroups, show_wcoa_edit_mapgroups
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
    # re_path(r'^collaborate/groups/(?P<pk>\d+)/(?P<slug>[\w-]+)/', MapGroupDetailView.as_view(template='wcoa/mapgroups/mapgroup_edit.html')(request), name='detail'),
    
    # re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/edit/remove-image$',
    #     RemoveMapGroupImageActionView.as_view(), name='remove-image'),
    # re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/$',
    #     MapGroupDetailView.as_view(), name='detail'),
    # re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/preferences$',
    #     MapGroupPreferencesView.as_view(), name='preferences'),
    # re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/join$',
    #     JoinMapGroupActionView.as_view(), name='join'),
    # re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/leave$',
    #     LeaveMapGroupActionView.as_view(), name='leave'),
    # re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/delete$',
    #     DeleteMapGroupActionView.as_view(), name='delete'),
    # re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/join$',
    #     RequestJoinMapGroupActionView.as_view(), name='request-join'),
    # re_path(r'^(?P<pk>\d+)/approve$',
    #     ApproveMapGroupActionView.as_view(), name='request-approve'),
    # re_path(r'^(?P<pk>\d+)/deny$',
    #     DenyMapGroupActionView.as_view(), name='request-deny'),
    # re_path(r'^(?P<pk>\d+)/promote$',
    #     PromoteMapGroupMemberActionView.as_view(), name='promote-member'),
    # re_path(r'^(?P<pk>\d+)/demote$',
    #     DemoteMapGroupMemberActionView.as_view(), name='demote-member'),
    # re_path(r'^(?P<pk>\d+)/remove$',
    #     RemoveMapGroupMemberActionView.as_view(), name='remove-member'),
    # re_path(r'^groups/create', create_wcoa_mapgroup, name='create_wcoa_mapgroup'),
    # re_path(r'^g/', RedirectView.as_view(url='/groups/')), # 301
    # re_path(r'^/$', views.index, name='index'),
]
