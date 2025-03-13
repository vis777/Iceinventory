# Generated by Django 5.1.6 on 2025-03-11 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Iceapp', '0005_remove_order_customer_remove_order_ice_stock'),
        ('Shopapp', '0014_remove_order_customer_remove_order_ice_stock_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='order',
        ),
        migrations.RemoveField(
            model_name='productdb',
            name='product_category',
        ),
        migrations.DeleteModel(
            name='IceStock',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='ProductDb',
        ),
    ]
