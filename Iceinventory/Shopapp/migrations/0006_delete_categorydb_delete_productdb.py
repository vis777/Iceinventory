# Generated by Django 5.1.6 on 2025-02-26 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shopapp', '0005_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CategoryDb',
        ),
        migrations.DeleteModel(
            name='ProductDb',
        ),
    ]
