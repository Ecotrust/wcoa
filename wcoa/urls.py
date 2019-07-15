from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'wcoa'
urlpatterns = [
    path('', views.index, name='index'),
]
