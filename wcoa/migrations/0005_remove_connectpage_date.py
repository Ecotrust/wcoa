# Generated by Django 2.2.3 on 2019-07-25 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wcoa', '0004_merge_20190725_1749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='connectpage',
            name='date',
        ),
    ]
