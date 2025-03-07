from django.db import models
from Iceapp.models import Order

# Category Model
class CategoryDb(models.Model):
    category_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)  # Increased field size for more details
    status = models.CharField(
        max_length=50,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active'
    )
    category_image = models.ImageField(upload_to="category_images", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Track creation time
    updated_at = models.DateTimeField(auto_now=True)  # Track last update

    def __str__(self):
        return self.category_name if self.category_name else "Unnamed Category"


# Product Model
class ProductDb(models.Model):
    product_category = models.ForeignKey(CategoryDb, on_delete=models.CASCADE)  # Establish relationship
    product_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Decimal for prices
    status = models.CharField(
        max_length=50,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active'
    )
    product_image = models.ImageField(upload_to="product_images", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name if self.product_name else "Unnamed Product"


# Ice Stock Model
class IceStock(models.Model):
    ice_type = models.ForeignKey(ProductDb, on_delete=models.CASCADE, related_name="ice_stock")  # Link to ProductDb
    quantity_kg = models.DecimalField(max_digits=10, decimal_places=2)  # In kg
    reorder_point = models.DecimalField(max_digits=10, decimal_places=2)  # Minimum threshold
    last_updated = models.DateTimeField(auto_now=True)

    def is_low_stock(self):
        return self.quantity_kg <= self.reorder_point

    def __str__(self):
        return f"{self.ice_type.product_name} - {self.quantity_kg} kg"


# Order Item Model (Allows multiple products in an order)
class OrderItem(models.Model):
    order = models.ForeignKey('Iceapp.Order', on_delete=models.CASCADE, related_name="order_items")  # Lazy import
    product = models.ForeignKey('ProductDb', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.order.id} - {self.product.product_name} ({self.quantity})"


# Payment Model
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status_choices = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed')
    ]
    payment_status = models.CharField(max_length=10, choices=payment_status_choices, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)  # For tracking online payments

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.payment_status}"