# Generated by Django 4.2 on 2024-02-29 00:07

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
import wcoa.models
import wcoa.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_portalrendition_file'),
        ('wcoa', '0023_ohiclass_ohiclass_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='ohicategory',
            name='ohicategory_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='base.portalimage'),
        ),
        migrations.AlterField(
            model_name='ohiindicatorpage',
            name='body',
            field=wagtail.fields.StreamField([('Score', wagtail.blocks.StructBlock([('state', wagtail.blocks.ChoiceBlock(choices=[('West Coast', 'West Coast'), ('CA', 'California'), ('OR', 'Oregon'), ('WA', 'Washington')])), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('year', wagtail.blocks.IntegerBlock(help_text='Year of the report', required=False)), ('report', wagtail.blocks.URLBlock(help_text='URL to the report', required=False))])), ('WYSIWYG', wagtail.blocks.RichTextBlock()), ('border', wcoa.blocks.CTARowDivider())], use_json_field=True),
        ),
    ]