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

class WCOALayerAdmin(LayerAdmin):
    list_display = ('name', 'layer_type', 'date_modified', 'Theme_', 'order', 'data_source', 'primary_site', 'preview_site', 'url')
    if settings.CATALOG_TECHNOLOGY not in ['Madrona', None]:
        # catalog_fields = ('catalog_name', 'catalog_id',)
        catalog_fields = 'catalog_name'
    else:
        catalog_fields = None
    fieldsets = (
        ('BASIC INFO', {
            'fields': (
                catalog_fields,
                ('name','layer_type',),
                ('url', 'proxy_url'),
                'site'
            )
        }),
        ('LAYER ORGANIZATION', {
            # 'classes': ('collapse','open',),
            'fields': (
                ('order','themes'),
                ('is_sublayer','sublayers'),
                ('has_companion','connect_companion_layers_to'),
                # RDH 2019-10-25: We don't use this, and it doesn't seem helpful
                # ('is_disabled','disabled_message')
            )
        }),
        ('METADATA & LINKS', {
            'classes': ('collapse',),
            'fields': (
                'description',
                ('kml', 'data_download'),
                ('metadata','source'),
                # RDH 2019-10-25: We don't use these, and it doesn't seem helpful
                # 'data_overview','data_source','data_notes', 'data_publish_date'
                # ('bookmark', 'kml'),
                # ('data_download','learn_more'),
                # ('map_tiles'),
            )
        }),
        ('LEGEND', {
            'classes': ('collapse',),
            'fields': (
                'show_legend',
                'legend',
                'legend_title',
                'legend_subtitle',
            )
        }),
        # ('SHARING', {
        #     'classes': ('collapse',),
        #     'fields': (
        #         'shareable_url',
        #     )
        # }),
        ('ArcGIS DETAILS', {
            'classes': ('collapse',),
            'fields': (
                ('arcgis_layers', 'query_by_point', 'disable_arcgis_attributes'),
            )
        }),
        ('WMS DETAILS', {
            'classes': ('collapse',),
            'fields': (
                'wms_help',
                ('wms_slug', 'wms_version'),
                ('wms_format', 'wms_srs'),
                ('wms_timing', 'wms_time_item'),
                ('wms_styles', 'wms_additional'),
                ('wms_info', 'wms_info_format'),
            )
        }),
        # ('Dynamic Layers (MDAT & CAS)', {
        #     'classes': ('collapse',),
        #     'fields': (
        #         'search_query',
        #     )
        # }),
        # ('UTF Grid Layers', {
        #     'classes': ('collapse',),
        #     'fields': (
        #         'utfurl',
        #     )
        # }),
        ('ATTRIBUTE REPORTING', {
            'classes': ('collapse',),
            'fields': (
                ('label_field'),
                # ('attribute_event', 'attribute_fields'),
                'attribute_fields',
                # ('lookup_field', 'lookup_table'),
                # ('mouseover_field'),
                # 'is_annotated',           # used for popovers, not implemented since OL2
                # 'compress_display',
            )
        }),
        ('DISPLAY & STYLE', {
            'classes': ('collapse',),
            'fields': (
                'opacity',
                (
                    'minZoom',
                    'maxZoom'
                ),
                'custom_style',
                (
                    'vector_outline_width',
                    'vector_outline_color', 
                    # 'vector_outline_opacity',
                ),
                (
                    'vector_fill',
                    'vector_color', 
                ),
                (
                    'point_radius',
                    'vector_graphic',
                    'vector_graphic_scale',
                ),
                (
                    'lookup_field',
                    'lookup_table',
                ),
                # 'thumbnail',
            )
        }),
        # ('ESPIS', {
        #     'classes': ('collapse',),
        #     'fields': (
        #         ('espis_enabled', 'espis_region'),
        #         ('espis_search' ),
        #     )
        # }),
    )

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
