from django.db import models
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.models import Image
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock

class LinkStructValue(blocks.StructValue):
    def url(self):
        external_url = self.get('external_url')
        page = self.get('page')
        if external_url:
            return external_url
        elif page:
            return page.url

class BrickBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    text = blocks.RichTextBlock()
    page = blocks.PageChooserBlock(label="page", required=False)
    external_url = blocks.URLBlock(label="external URL", required=False)
    photo = ImageChooserBlock(required=False)

    class Meta:
        icon = 'page'
        value_class = LinkStructValue

class CTAStreamBlock(blocks.StructBlock):
    cta_title = blocks.CharBlock()
    cta_content = blocks.RichTextBlock()
    cta_link = blocks.URLBlock(label="URL",required=False)

    class Meta:
        icon = 'cogs'

class MasonryPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="block-title")),
        ('text', blocks.RichTextBlock()),
        ('brick', BrickBlock()),
        ('image', ImageChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

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
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    cta_list = StreamField([
        ('connection', CTAStreamBlock()),
        ('details', blocks.RichTextBlock()),
    ])

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
        ImageChooserPanel('body_image'),
        StreamFieldPanel('cta_list'),
    ]
