from django.contrib import admin
from django.urls import include, path

from . import views

app_name = 'wcoa'
urlpatterns = [
    # path('', views.index, name='index'),
    path('/', views.index, name='index'),
    path('admin/', admin.site.urls),
]
