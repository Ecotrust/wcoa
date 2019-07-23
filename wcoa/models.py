from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock

class CTAStreamBlock(blocks.StructBlock):
    cta_title = blocks.CharBlock()
    cta_content = blocks.RichTextBlock()
    cta_link = blocks.URLBlock(label="URL",required=False)

    class Meta:
        icon='cogs'

class ConnectPage(Page):

    # Database fields

    grid_cta_one = RichTextField()
    grid_cta_two = RichTextField()
    grid_cta_three = RichTextField()

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

    date = models.DateField("Post date")

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldRowPanel([
            FieldPanel('grid_cta_one'),
            FieldPanel('grid_cta_two'),
            FieldPanel('grid_cta_three'),
        ]),
        FieldPanel('body'),
        ImageChooserPanel('body_image'),
        StreamFieldPanel('cta_list'),
    ]
