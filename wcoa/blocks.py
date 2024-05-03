from django.conf import settings
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock

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
    width = blocks.IntegerBlock(required=False,max_value=12,min_value=0,help_text='Number of columns to span out of 12 (e.g., input of 3 would mean give this a width of 3 out of the 12 (25%))')
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

class OHIIndicatorScore(blocks.StructBlock):
    state = blocks.ChoiceBlock(choices=[
        ('West Coast', 'West Coast'),
        ('CA', 'California'),
        ('OR', 'Oregon'),
        ('WA', 'Washington'),
    ])
    image = ImageChooserBlock(required=False)
    year = blocks.IntegerBlock(required=False, help_text='Year of the report')
    report = blocks.URLBlock(required=False, help_text='URL to the report')
    indicator_page = ParentalKey('IndicatorPage', on_delete=models.CASCADE, related_name='indicator_scores')

    class Meta:
        template = 'wcoa/blocks/ohi_indicator_score.html'

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
        ('rgba(255,255,255,1)', 'White'),
        ('rgba(0,0,0,1)', 'Black'),
        ('rgba(48, 112, 247, 1)', 'Blue'),
        ('rgba(152, 171, 55, 1)', 'Green'),
        ('rgba(242,191,76,1)', 'Yellow'),
        ('rgba(250, 35, 18, 1)', 'Red'),
        ('rgba(77,77,79,1)', 'Grey'),
    ]

    background_color_choices = [
        ('rgba(255, 255, 255, 1)', 'White'),
        ('rgba(0, 0, 0, 0.5)', 'Black'),
        ('rgba(48, 112, 247, 0.5)', 'Blue'),
        ('rgba(152, 171, 55, 0.5)', 'Green'),
        ('rgba(242, 191, 76, 0.5)', 'Yellow'),
        ('rgba(250, 35, 18, 0.5)', 'Red'),
        ('rgba(77, 77, 79, 0.5)', 'Grey'),
    ]

    content = blocks.StreamBlock([
        ('Score', OHIIndicatorScore()),
        ('WYSIWYG', blocks.RichTextBlock(required=False)),
    ], required=False, use_json_field=True)

    full_image = ImageChooserBlock(required=False)
    text_color = blocks.ChoiceBlock(choices=color_choices, default='black', icon='color_palette', required=False)
    background_color = blocks.ChoiceBlock(choices=background_color_choices, default='white', icon='color', required=False)
    border_color = blocks.ChoiceBlock(choices=color_choices, default='', icon='color_palette', required=False)
    border_width = blocks.IntegerBlock(default='', help_text='Width of the border in pixels', required=False, min_value=0, max_value=10)
    link = blocks.URLBlock(required=False, help_text='Wrap column in a link')

    class Meta:
        template = 'wcoa/blocks/ohi_struct_block.html'
