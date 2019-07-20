from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
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
