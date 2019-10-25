from django.conf import settings
from django.contrib import admin
from django import forms
from data_manager.models import *
from data_manager.admin import ThemeAdmin, LayerAdmin, AttributeInfoAdmin, AttributeInfoAdmin, LookupInfoAdmin, DataNeedAdmin

class WCOAThemeAdmin(ThemeAdmin):
    list_display = ('display_name', 'name', 'order', 'primary_site', 'preview_site')
    fields= (
        'site',
        'display_name',
        'name',
        'order',
        'visible',
    )

if not settings.DATA_MANAGER_ADMIN:
    admin.site.register(Theme, WCOAThemeAdmin)
    admin.site.register(Layer, LayerAdmin)
    admin.site.register(AttributeInfo, AttributeInfoAdmin)
    admin.site.register(LookupInfo, LookupInfoAdmin)
    admin.site.register(DataNeed, DataNeedAdmin)
