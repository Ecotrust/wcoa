# Generated by Django 2.2.3 on 2019-07-25 23:13

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wcoa', '0007_auto_20190725_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectpage',
            name='cta_list',
            field=wagtail.core.fields.StreamField([('connection', wagtail.core.blocks.StructBlock([('cta_title', wagtail.core.blocks.CharBlock()), ('cta_content', wagtail.core.blocks.RichTextBlock()), ('cta_link', wagtail.core.blocks.URLBlock(label='URL', required=False)), ('width', wagtail.core.blocks.IntegerBlock(help_text='Number of columns to span out of 12 (e.g., input of 3 would mean give this a width of 3 out of the 12 (25%))', max_value=12, min_value=0, required=False)), ('background_color', wagtail.core.blocks.ChoiceBlock(choices=[('blue', 'Blue'), ('green', 'Green')], icon='color')), ('background_image', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('details', wagtail.core.blocks.RichTextBlock())]),
        ),
        migrations.AlterField(
            model_name='ctapage',
            name='body',
            field=wagtail.core.fields.StreamField([('item', wagtail.core.blocks.StructBlock([('cta_title', wagtail.core.blocks.CharBlock()), ('cta_content', wagtail.core.blocks.RichTextBlock()), ('cta_link', wagtail.core.blocks.URLBlock(label='URL', required=False)), ('width', wagtail.core.blocks.IntegerBlock(help_text='Number of columns to span out of 12 (e.g., input of 3 would mean give this a width of 3 out of the 12 (25%))', max_value=12, min_value=0, required=False)), ('background_color', wagtail.core.blocks.ChoiceBlock(choices=[('blue', 'Blue'), ('green', 'Green')], icon='color')), ('background_image', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('details', wagtail.core.blocks.RichTextBlock())]),
        ),
    ]
