from django.contrib import admin
from django.urls import include, path

from . import views
from wagtailimportexport import urls as wagtailimportexport_urls

app_name = 'wcoa'
urlpatterns = [
    # path('', views.index, name='index'),
    path('/', views.index, name='index'),
    # ...
    url(r'', include(wagtailimportexport_urls)),
    url(r'', include(wagtail_urls)),
]
