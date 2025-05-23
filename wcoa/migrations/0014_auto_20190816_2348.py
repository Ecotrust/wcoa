# Generated by Django 2.2.3 on 2019-08-16 23:48

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
import wcoa.models
import wcoa.blocks

class Migration(migrations.Migration):

    dependencies = [
        ('wcoa', '0013_auto_20190816_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ctapage',
            name='body',
            field=wagtail.fields.StreamField([('item', wagtail.blocks.StructBlock([('cta_title', wagtail.blocks.CharBlock(required=False)), ('cta_content', wagtail.blocks.RichTextBlock(required=False)), ('cta_page', wagtail.blocks.PageChooserBlock(label='page', required=False)), ('cta_link', wagtail.blocks.URLBlock(label='URL', required=False)), ('width', wagtail.blocks.IntegerBlock(help_text='Number of columns to span out of 12 (e.g., input of 3 would mean give this a width of 3 out of the 12 (25%))', max_value=12, min_value=0, required=False)), ('text_color', wagtail.blocks.ChoiceBlock(choices=[('white', 'White'), ('black', 'Black'), ('blue', 'Blue'), ('green', 'Green'), ('red', 'Red'), ('purple', 'Purple'), ('grey', 'Grey')], icon='color_palette', required=False)), ('background_color', wagtail.blocks.ChoiceBlock(choices=[('white', 'White'), ('black', 'Black'), ('blue', 'Blue'), ('green', 'Green'), ('red', 'Red'), ('purple', 'Purple'), ('grey', 'Grey')], icon='color', required=False)), ('background_image', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('details', wagtail.blocks.RichTextBlock()), ('row', wcoa.blocks.CTARowDivider())]),
        ),
    ]
