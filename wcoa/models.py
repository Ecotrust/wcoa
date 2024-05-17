from django.conf import settings
from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from portal.home.models import HomePage
from portal.base.models import PortalImage, DetailPageBase, PageBase, MediaItem
from portal.calendar.models import Calendar
from portal.news.models import News
from portal.ocean_stories.models import OceanStory, OceanStories
from portal.grid_pages.models import GridPage, GridPageDetail, GridPageSection, GridPageSectionBase
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from wagtail.images.models import Image
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from wcoa import blocks as wcoa_blocks

class CTAPage(Page):
    body = StreamField(
        [
            ('item', wcoa_blocks.CTAStreamBlock()),
            ('details', blocks.RichTextBlock()),
            ('row', wcoa_blocks.CTARowDivider()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    subpage_types = [
        'wcoa.CTAPage',
        'grid_pages.GridPage',
        'calendar.Calendar',
        'news.News',
        'wcoa.WcoaOceanStories',
        'wcoa.ConnectPage',
        'wcoa.CatalogIframePage',
        'wcoa.CatalogThemeGridPage',
        'pages.Page',
        'wcoa.OHIDashboard',
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['CATALOG_QUERY_ENDPOINT'] = settings.CATALOG_QUERY_ENDPOINT

        return context


class ConnectPage(Page):

    # Database fields

    grid_cta_one_title = models.CharField(max_length=255,null=True,blank=True)
    grid_cta_one = models.CharField(max_length=255,null=True,blank=True)
    grid_cta_two_title = models.CharField(max_length=255,null=True,blank=True)
    grid_cta_two = models.CharField(max_length=255,null=True,blank=True)
    grid_cta_three_title = models.CharField(max_length=255,null=True,blank=True)
    grid_cta_three = models.CharField(max_length=255,null=True,blank=True)

    body = RichTextField()
    body_image = models.ForeignKey(
        PortalImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    cta_list = StreamField(
        [
            ('connection', wcoa_blocks.CTAStreamBlock()),
            ('details', blocks.RichTextBlock()),
        ],
        use_json_field=True,
    )

    # Editor panels configuration

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('grid_cta_one_title'),
                FieldPanel('grid_cta_one'),
                FieldPanel('grid_cta_two_title'),
                FieldPanel('grid_cta_two'),
                FieldPanel('grid_cta_three_title'),
                FieldPanel('grid_cta_three'),
            ],
            heading="Top of page calls to action",
            classname="collapsible",
        ),
        FieldPanel('body'),
        FieldPanel('body_image'),
        FieldPanel('cta_list'),
    ]


class CatalogIframePage(Page):
    # 255 is too short for much "DSL" queries to support GP2 + Elasticsearch
    # SO says <2000 is a good guideline: https://stackoverflow.com/a/417184/706797
    source = models.URLField(max_length=1999)

    content_panels = Page.content_panels + [
        FieldPanel('source')
    ]

class CatalogThemeGridPage(GridPage):
    subpage_types = ['CatalogThemeGridPageDetail']

    def get_detail_children(self):
        return CatalogThemeGridPageDetail.objects.child_of(self)

class CatalogThemeGridPageDetail(GridPageDetail):
    parent_page_types = ['CatalogThemeGridPage']
    theme = models.CharField(max_length=255, blank=True, null=True)

    search_fields = DetailPageBase.search_fields + (
        index.SearchField('description'),
        index.FilterField('metric'),
        index.SearchField('theme')
    )

    content_panels = DetailPageBase.content_panels + [
        FieldPanel('metric'),
        FieldPanel('theme')
    ]

class WcoaOceanStories(OceanStories):
    subpage_types = ['WcoaOceanStory']

    def get_detail_children(self):
        return WcoaOceanStory.objects.child_of(self)

class WcoaOceanStory(OceanStory):
    parent_page_types = ['WcoaOceanStories']

# OCEAN HEALTH INDEX OHI PAGES 
class OHIDashboard(Page):
    """
    A page model for displaying the Ocean Health dashboard.

    This model allows the creation of the root Ocean Health dashboard page.

    Attributes:
        name (str): name displayed on UI
        description (str): meta description for SEO
        ohilogo (ForeignKey): image for the dashboard

    """

    page_description = "Use this for the root Ocean Health dashboard page."
    ohi_logo = models.ForeignKey(
        PortalImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    body = StreamField(
        [
            ('content', blocks.RichTextBlock(required=False)),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('ohi_logo'),
        FieldPanel('body'),
    ]

    subpage_types = [
        'wcoa.OHICategory',
    ]

    def get_ohi_hierarchy_dict(self):
        cat_dict = {}
        for cat in self.get_children().specific():
            theme_dict = {}
            for theme in cat.get_children().specific():
                indicator_dict = {}
                for indicator in theme.get_children().specific():
                    indicator_dict[indicator.title] = {
                        'title': indicator.title,
                        'img': indicator.img.file.url if indicator.img else None, 
                        'url': indicator.url,
                    }
                theme_dict[theme.title] = {
                    'title': theme.title, 
                    'img': theme.img.file.url if theme.img else None, 
                    'url': theme.url,
                    'indicators': indicator_dict
                }
            cat_dict[cat.title] = {
                'title': cat.title,
                'img': cat.img.file.url if cat.img else None,
                'url': cat.url,
                'classes': theme_dict
            }
        hierarchy_dict = {
            'title': 'Ocean Health Index',
            'categories': cat_dict
        }
        
        return hierarchy_dict

    def get_child_categories(self):
        # Get list of categories in this dashboard
        categories = OHICategory.objects.live().descendant_of(self)
        return categories
    
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        hierarchy_dict = self.get_ohi_hierarchy_dict()
        context['ohi_hierarchy_dict'] = hierarchy_dict
        return context

class OHICategory(Page):
    """
    Represents an indicator category.

    Attributes:
        page_description (str): The description of the page.
        TODO

    Methods:
        get_child_classes(): Returns a list of child classes (OHIClass) of this category.
        #TODO
    """

    page_description = "Use this to create an indicator category."
    img = models.ForeignKey(
        PortalImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('img'),
    ]

    subpage_types = [
        'wcoa.OHIClass',
    ]

    def get_child_classes(self):
        # Get list of indicators in this category
        classes = OHIClass.objects.live().descendant_of(self)
        return classes

    def get_class_indicators(self):
        classes = self.get_child_classes()
        indicators = []
        for c in classes:
            indicators += OHIIndicatorPage.objects.live().descendant_of(c)
        return indicators
        
class OHIClass(Page):
    """
    An indicator class.

    Attributes:
    TODO

    """

    page_description = "Use this to create a indicator class."
    img = models.ForeignKey(
        PortalImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('img'),
    ]

    subpage_types = [
        'wcoa.OHIIndicatorPage',
    ]

    def get_child_indicators(self):
        # Get list of categories in this class
        indicators = OHIIndicatorPage.objects.live().descendant_of(self)
        return indicators


class OHIIndicatorPage(Page):
    """
    OHI Indicator Page

    Attributes:
    TODO

    """

    page_description = "Use the to create a page for an indicator."
    img = models.ForeignKey(
        PortalImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    body = StreamField(
        [
            ('Clear', wcoa_blocks.CTARowDivider()),
            ('Column', wcoa_blocks.OHIStuctBlock()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('img'),
        FieldPanel('body'),
    ]

    subpage_types = [
        'wcoa.OHIIndicatorPage',
    ]

    def get_indicator_class(self):
        # Find the indicator category that is an ancestor of this page
        return self.get_ancestors().type(OHIClass).last()


WcoaOceanStory.content_panels = DetailPageBase.content_panels + [
    FieldPanel('display_home_page'),
    MultiFieldPanel([FieldPanel('hook'), FieldPanel('explore_title'), FieldPanel('explore_url')], "Map overlay"),
    InlinePanel('sections', label="Sections" ),
]

wcoa_appropriate_subpage_types = [
    # removes Ocean Stories, Data Catalog, and Data Gaps from defaultm adds wcoa pages
    'calendar.Calendar',
    'wcoa.CatalogIframePage',
    'wcoa.CatalogThemeGridPage',
    'wcoa.ConnectPage',
    'wcoa.CTAPage',
    'grid_pages.GridPage',
    'news.News',
    'pages.Page',
    'wcoa.WcoaOceanStories',
    'wcoa.OHIDashboard',
]
Page.subpage_types = wcoa_appropriate_subpage_types
# These should not be viable Root Pages
Calendar.parent_page_types = ['wcoa.CTAPage','pages.Page',]
News.parent_page_types = ['wcoa.CTAPage','pages.Page',]
