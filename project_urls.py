from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('wcoa/', include('wcoa.urls')),
    path('admin/', admin.site.urls),
]
