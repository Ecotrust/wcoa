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

try:
    from .local_settings import *
except ImportError:
    print(
        "we recommend using a local settings file; "\
        "`cp local_settings.template local_settings.py` and modify as needed"
    )
    pass
