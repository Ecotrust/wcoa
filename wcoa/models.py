from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index

class ConnectPage(Page):

    # Database fields

    grid_cta_one = RichTextField()
    grid_cta_two = RichTextField()
    grid_cta_three = RichTextField()

    body = RichTextField()
    body_image = cover = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    cta_list = StreamField([
        ('cta_list_block', blocks.StreamBlock([
            blocks.StructBlock([
                ('title', blocks.CharBlock()),
                ('paragraph', blocks.RichTextBlock(required=False)),
                ('link', blocks.URLBlock(label="URL",required=False)
            ]),
            blocks.StructBlock([
                ('paragraph', blocks.RichTextBlock()),
            ]),
        ])),
    ])

    date = models.DateField("Post date")
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),
    ]

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldRowPanel([
            'grid_cta_three',
            'grid_cta_three',
            'grid_cta_three',
        ]),
        FieldPanel('body', classname="full"),
        ImageChooserPanel('body_image'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
    ]
