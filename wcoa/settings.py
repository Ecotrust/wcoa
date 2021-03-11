from visualize.settings import *
from data_manager.settings import *

PROJECT_REGION = {
    'name': 'West Coast',
    'init_zoom': 5,
    'init_lat': 40.5,
    'init_lon': -124.5,
    'srid': 4326,
    'map': 'ocean',
}

CATALOG_SOURCE = 'http://192.168.0.3:9200'

CATALOG_QUERY_ENDPOINT = '/geoportal/elastic/metadata/item/_search/'

DATA_MANAGER_ADMIN = False

DATA_CATALOG_ENABLED = False

CATALOG_TECHNOLOGY = 'GeoPortal2'

HANDLER_404 = 'wcoa.views.page_not_found'

WAGTAILEMBEDS_FINDERS = [
    {
        'class': 'wagtail.embeds.finders.oembed',
        'providers': [
            {
                "endpoint": "https://www.youtube.com/oembed",
                "urls": [
                    r'^https?://(?:[-\w]+\.)?youtube\.com/watch.+$',
                    r'^https?://(?:[-\w]+\.)?youtube\.com/v/.+$',
                    r'^https?://youtu\.be/.+$',
                    r'^https?://(?:[-\w]+\.)?youtube\.com/user/.+$',
                    r'^https?://(?:[-\w]+\.)?youtube\.com/[^#?/]+#[^#?/]+/.+$',
                    r'^https?://m\.youtube\.com/index.+$',
                    r'^https?://(?:[-\w]+\.)?youtube\.com/profile.+$',
                    r'^https?://(?:[-\w]+\.)?youtube\.com/view_play_list.+$',
                    r'^https?://(?:[-\w]+\.)?youtube\.com/playlist.+$',
                ],
            }
        ],
        'options': {'scheme': 'https'}
    },
    {
        'class': 'wagtail.embeds.finders.oembed',
    }
]

try:
    from .local_settings import *
except ImportError:
    print(
        "we recommend using a local settings file; "\
        "`cp local_settings.template local_settings.py` and modify as needed"
    )
    pass
