# Generated by Django 2.2.3 on 2019-07-20 00:01

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wcoa', '0002_auto_20190719_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masonrypage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(classname='block-title')), ('text', wagtail.blocks.RichTextBlock()), ('brick', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('text', wagtail.blocks.RichTextBlock()), ('page', wagtail.blocks.PageChooserBlock(label='page', required=False)), ('external_url', wagtail.blocks.URLBlock(label='external URL', required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False))])), ('image', wagtail.images.blocks.ImageChooserBlock())]),
        ),
    ]
