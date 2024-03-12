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
        'wcoa.OHICategory',
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

    # search_fields = (index.SearchField('description'),)

    def get_detail_children(self):
        return WcoaOceanStory.objects.child_of(self)

class WcoaOceanStory(OceanStory):
    parent_page_types = ['WcoaOceanStories']

class OHIStuctBlock(blocks.StructBlock):
    # width is an int in CTA blocks, but a choice block is preferrable
    width = blocks.ChoiceBlock(choices=[
        ('1', '1/12'),
        ('2', '2/12'),
        ('3', '3/12'),
        ('4', '4/12'),
        ('5', '5/12'),
        ('6', '6/12'),
        ('7', '7/12'),
        ('8', '8/12'),
        ('9', '9/12'),
        ('10', '10/12'),
        ('11', '11/12'),
        ('12', '12/12'),
    ], default='12', label='Width', icon='arrow-right', required=False)

    color_choices = [
        ('white', 'White'),
        ('black', 'Black'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('red', 'Red'),
        ('purple', 'Purple'),
        ('grey', 'Grey'),
    ]

    # content = blocks.RichTextBlock(required=False)
    content = blocks.StreamBlock([
        ('Score', wcoa_blocks.OHIIndicatorScore()),
        ('WYSIWYG', blocks.RichTextBlock(required=False)),
    ], required=False, use_json_field=True)

    text_color = blocks.ChoiceBlock(choices=color_choices, default='black', icon='color_palette', required=False)
    background_color = blocks.ChoiceBlock(choices=color_choices, default='white', icon='color', required=False)
    background_image = ImageChooserBlock(required=False)
    border_color = blocks.ChoiceBlock(choices=color_choices, default='', icon='color_palette', required=False)
    border_width = blocks.IntegerBlock(default='', help_text='Width of the border in pixels', required=False, min_value=0, max_value=10)
    link = blocks.URLBlock(required=False, help_text='Wrap column in a link')

    class Meta:
        template = 'wcoa/blocks/ohi_struct_block.html'

class OHIIndicatorPage(Page):
    page_description = "Use the to create a page for an indicator."
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)
    indicator_image = models.ForeignKey(
        PortalImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    body = StreamField(
        [
            ('Clear', wcoa_blocks.CTARowDivider()),
            ('Column', OHIStuctBlock()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('indicator_image'),
        FieldPanel('body'),
        FieldPanel('description'),
    ]

    def get_indicator_class(self):
        # Find the indicator category that is an ancestor of this page
        return self.get_ancestors().type(OHIClass).last()

class OHIClass(Page):
    page_description = "Use this to create a indicator class."
    name = models.CharField(max_length=255)
    ohiclass_image = models.ForeignKey(
        PortalImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('ohiclass_image'),
    ]

    subpage_types = [
        'wcoa.OHIIndicatorPage',
    ]

    def get_child_indicators(self):
        # Get list of categories in this class
        indicators = OHIIndicatorPage.objects.live().descendant_of(self)
        return indicators

class OHICategory(Page):
    page_description = "Use this to create a indicator category."
    name = models.CharField(max_length=255)
    ohicategory_image = models.ForeignKey(
        PortalImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('ohicategory_image'),
    ]

    subpage_types = [
        'wcoa.OHIClass',
    ]

    def get_child_classes(self):
        # Get list of indicators in this category
        classes = OHIClass.objects.live().descendant_of(self)
        return classes


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
    'wcoa.OHICategory',
    'wcoa.OHIIndicatorPage',
]
Page.subpage_types = wcoa_appropriate_subpage_types
# These should not be viable Root Pages
Calendar.parent_page_types = ['wcoa.CTAPage','pages.Page',]
News.parent_page_types = ['wcoa.CTAPage','pages.Page',]
