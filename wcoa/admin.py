from django.conf import settings
from django.contrib import admin
from django import forms
from data_manager.models import AttributeInfo, LookupInfo, DataNeed
from layers.models import Theme, Layer
from data_manager.admin import AttributeInfoAdmin, AttributeInfoAdmin, LookupInfoAdmin, DataNeedAdmin
from layers.admin import ThemeAdmin, LayerAdmin

class WCOAThemeAdmin(ThemeAdmin):
    list_display = ('display_name', 'name', 'order', 'primary_site', 'preview_site')

class WCOALayerAdmin(LayerAdmin):
    list_display = ('name', 'layer_type', 'date_modified', 'get_parent_themes', 'get_order', 'data_source', 'primary_site', 'preview_site', 'http_status', 'last_success_status', 'url')
    if settings.CATALOG_TECHNOLOGY not in ['Madrona', None]:
        # catalog_fields = ('catalog_name', 'catalog_id',)
        catalog_fields = 'catalog_name'
    else:
        catalog_fields = None

if not settings.DATA_MANAGER_ADMIN:
    admin.site.unregister(Theme)
    admin.site.register(Theme, WCOAThemeAdmin)
    admin.site.unregister(Layer)
    admin.site.register(Layer, WCOALayerAdmin)
    admin.site.unregister(AttributeInfo)
    admin.site.register(AttributeInfo, AttributeInfoAdmin)
    admin.site.unregister(LookupInfo)
    admin.site.register(LookupInfo, LookupInfoAdmin)
    # admin.site.register(DataNeed, DataNeedAdmin)
