# Generated by Django 5.1.6 on 2025-02-26 10:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shopapp', '0010_remove_orderitem_order_remove_payment_order_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_ordered', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('delivered', 'Delivered'), ('canceled', 'Canceled')], default='pending', max_length=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shopapp.customer')),
                ('ice_stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shopapp.icestock')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='Shopapp.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shopapp.productdb')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed')], default='pending', max_length=10)),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Shopapp.order')),
            ],
        ),
    ]
