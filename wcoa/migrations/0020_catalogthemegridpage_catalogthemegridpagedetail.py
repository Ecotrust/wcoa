# Generated by Django 2.2.9 on 2021-02-23 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grid_pages', '0005_auto_20190710_0058'),
        ('wcoa', '0019_auto_20200922_1837'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogThemeGridPage',
            fields=[
                ('gridpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='grid_pages.GridPage')),
            ],
            options={
                'abstract': False,
            },
            bases=('grid_pages.gridpage',),
        ),
        migrations.CreateModel(
            name='CatalogThemeGridPageDetail',
            fields=[
                ('gridpagedetail_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='grid_pages.GridPageDetail')),
                ('theme', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('grid_pages.gridpagedetail',),
        ),
    ]