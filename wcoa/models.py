from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from wagtail.images.models import Image
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from portal.home.models import HomePage
from portal.base.models import PortalImage, DetailPageBase, PageBase, DetailPageBase, MediaItem
from portal.calendar.models import Calendar
from portal.news.models import News
from portal.ocean_stories.models import OceanStory, OceanStories
from portal.grid_pages.models import GridPage, GridPageDetail, GridPageSection, GridPageSectionBase
from django.conf import settings

class LinkStructValue(blocks.StructValue):
    def url(self):
        external_url = self.get('cta_link')
        page = self.get('cta_page')
        if external_url:
            return external_url
        elif page:
            return page.url

class BrickBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    text = blocks.RichTextBlock(required=False)
    page = blocks.PageChooserBlock(label="page", required=False)
    external_url = blocks.URLBlock(label="external URL", required=False)
    photo = ImageChooserBlock(required=False)

    class Meta:
        icon = 'page'
        value_class = LinkStructValue

class CTARowDivider(blocks.StaticBlock):
    class Meta:
        icon = 'horizontalrule'
        label = 'Row divider'
        admin_text = 'Forces a new row to be created'

class CTAStreamBlock(blocks.StructBlock):
    cta_title = blocks.CharBlock(required=False)
    cta_content = blocks.RichTextBlock(required=False)
    cta_page = blocks.PageChooserBlock(label="page", required=False)
    cta_link = blocks.URLBlock(label="URL",required=False)
    # Width would be better as a CoiceBlock
    width = blocks.IntegerBlock(required=False,max_value=12,min_value=0,help_text="Number of columns to span out of 12 (e.g., input of 3 would mean give this a width of 3 out of the 12 (25%))")
    text_color = blocks.ChoiceBlock(choices=[
        ('white', 'White'),
        ('black', 'Black'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('red', 'Red'),
        ('purple', 'Purple'),
        ('grey', 'Grey'),
    ], icon='color_palette', required=False)
    background_color = blocks.ChoiceBlock(choices=[
        ('white', 'White'),
        ('black', 'Black'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('red', 'Red'),
        ('purple', 'Purple'),
        ('grey', 'Grey'),
    ], icon='color', required=False)
    background_image = ImageChooserBlock(required=False)

    class Meta:
        icon = 'form'
        value_class = LinkStructValue

class CTAPage(Page):
    body = StreamField(
        [
            ('item', CTAStreamBlock()),
            ('details', blocks.RichTextBlock()),
            ('row', CTARowDivider()),
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
            ('connection', CTAStreamBlock()),
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

    # search_fields = (index.SearchField('description'),)

    def get_detail_children(self):
        return WcoaOceanStory.objects.child_of(self)

class WcoaOceanStory(OceanStory):
    parent_page_types = ['WcoaOceanStories']

class IndicatorPage(StreamFieldPage):
    body = StreamField(
        [
            ('Content Block', CTAStreamBlock()),
            ('Rich Text Block', blocks.RichTextBlock()),
            ('Row Divider', CTARowDivider()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    parent_page_types = ['IndicatorCategory']

class IndicatorCategory(StreamFieldPage):
    subpage_types = ['IndicatorPage']

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
]
Page.subpage_types = wcoa_appropriate_subpage_types
# These should not be viable Root Pages
Calendar.parent_page_types = ['wcoa.CTAPage','pages.Page',]
News.parent_page_types = ['wcoa.CTAPage','pages.Page',]
