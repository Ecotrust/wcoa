PROJECT_REGION = {
    'name': 'West Coast',
    'init_zoom': 5,
    'init_lat': 40.5,
    'init_lon': -124.5,
    'srid': 4326,
    'map': 'ocean',
}

GEOPORTAL_VERSION = 129

SOLR_COLLECTION = 'collection129'

SOLR_ENDPOINT = 'https://portal.westcoastoceans.org/solr/%s/select?' % SOLR_COLLECTION

DATA_MANAGER_ADMIN = False

DATA_CATALOG_ENABLED = False

HANDLER_404 = 'wcoa.views.page_not_found'
