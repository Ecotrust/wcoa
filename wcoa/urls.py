from django.contrib import admin, auth
from django.urls import include, path, re_path
from django.views.generic import RedirectView

from . import views
from mapgroups import views as groupviews

app_name = 'wcoa'
handler404 = 'wcoa.views.page_not_found'
urlpatterns = [
    # path('', views.index, name='index'),
    re_path(r'^planner/?', views.show_wcoa_planner, name="planner_planner"),
    re_path(r'^visualize/?$', views.show_wcoa_planner, name="planner"),
    re_path(r'^embed/map/?', views.show_wcoa_embedded_map, name="show_wcoa_embedded_map"),
    re_path(r'^search/', views.search, name='search'),
    ### Accounts ###
    re_path(r'^account/?', views.show_wcoa_account_index, name="show_wcoa_account_indexs"),
    re_path(r'^account/edit/?', views.edit_account.as_view(), name="edit_account"),
    re_path(r'^account/change-password/?', views.ChangePasswordView.as_view(), name='change_password'),
    re_path(r'^account/register/?', views.register, name='register'),
    re_path(r'^account/forgot/?', views.forgot, name='forgot_password'),
    re_path(r'^account/forgot/(?P<code>[a-f0-9]{32})$', views.forgot_reset, name='forgot_reset'),
    re_path(r'^account/login/?', RedirectView.as_view(pattern_name='show_wcoa_account_indexs'), name='login'),
    re_path(r'^account/logout/?', auth.views.LogoutView.as_view(next_page='/'), name='logout'),
    # Map Groups
    re_path(r'^collaborate/groups/?', views.show_wcoa_mapgroups, name='show_wcoa_mapgroups'),
    re_path(r'^collaborate/groups/create/?', views.create_wcoa_mapgroup, name='create_wcoa_mapgroup'),
    re_path(r'^collaborate/groups/(?P<pk>\d+)/approve/?', groupviews.ApproveMapGroupActionView.as_view(), name='request-approve'),
    re_path(r'^collaborate/groups/(?P<pk>\d+)/deny/?', groupviews.DenyMapGroupActionView.as_view(), name='request-deny'),
    re_path(r'^collaborate/groups/(?P<pk>\d+)/promote/?', groupviews.PromoteMapGroupMemberActionView.as_view(), name='promote-member'),
    re_path(r'^collaborate/groups/(?P<pk>\d+)/demote/?', groupviews.DemoteMapGroupMemberActionView.as_view(), name='demote-member'),
    re_path(r'^collaborate/groups/(?P<pk>\d+)/remove/?', groupviews.RemoveMapGroupMemberActionView.as_view(), name='remove-member'),
    re_path(r'^collaborate/groups/(?P<pk>\d+)/(?P<slug>[\w-]+)/?', views.show_wcoa_detail_mapgroups, name='detail'),
    re_path(r'^collaborate/groups/(?P<pk>\d+)/(?P<slug>[\w-]+)/edit/?', views.show_wcoa_edit_mapgroups, name='edit'),
    re_path(r'^groups/?', views.show_wcoa_mapgroups, name='show_wcoa_mapgroups'),
    re_path(r'^groups/(?P<pk>\d+)/(?P<slug>[\w-]+)/edit/?', views.show_wcoa_edit_mapgroups, name='edit'),
    re_path(
        "choose-newtab-link/",
        views.NewTabLinkView.as_view(),
        name="wagtailadmin_choose_page_newtab_link",
    ),
    # path(
    #     "choose-external-link/",
    #     views.ExternalPlusLinkView.as_view(),
    #     name="wagtailadmin_choose_page_external_link",
    # ),
    # re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/join$',
    #     JoinMapGroupActionView.as_view(), name='join'),
    # re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/leave$',
    #     LeaveMapGroupActionView.as_view(), name='leave'),
    # re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/delete$',
    #     DeleteMapGroupActionView.as_view(), name='delete'),
    # re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/join$',
    #     RequestJoinMapGroupActionView.as_view(), name='request-join'),
    # re_path(r'^groups/create', views.create_wcoa_mapgroup, name='create_wcoa_mapgroup'),
    # re_path(r'^g/', RedirectView.as_view(url='/groups/')), # 301
    # re_path(r'^/$', views.index, name='index'),
]

def urls(namespace='wcoa'):
    """Returns a 3-tuple for use with include().

    The including module or project can refer to urls as namespace:urlname,
    internally, they are referred to as app_name:urlname.
    """
    return (urlpatterns, 'wcoa', namespace)
