# Generated by Django 5.1.6 on 2025-02-26 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shopapp', '0009_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
