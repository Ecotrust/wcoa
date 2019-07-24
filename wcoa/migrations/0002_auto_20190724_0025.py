# Generated by Django 2.2.3 on 2019-07-24 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wcoa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='connectpage',
            name='grid_cta_one_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='connectpage',
            name='grid_cta_three_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='connectpage',
            name='grid_cta_two_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='connectpage',
            name='grid_cta_one',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='connectpage',
            name='grid_cta_three',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='connectpage',
            name='grid_cta_two',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
