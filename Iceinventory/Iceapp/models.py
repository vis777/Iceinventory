from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional for authentication
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    address = models.TextField()
    preferences = models.TextField(blank=True)  # Special requests, preferred delivery time
    is_active = models.BooleanField(default=True)  # Allows deactivating customers instead of deleting them
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.JSONField(default=list)  # Store products & quantities
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    def update_status(self, new_status):
        """Update order status and set delivery date if delivered."""
        self.status = new_status
        if new_status == "Delivered":
            self.delivery_date = datetime.now()
        self.save()

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"



class ContactDb(models.Model):
    Contact_Name = models.CharField(max_length=100, null=True, blank=True)
    Contact_Email = models.CharField(max_length=100, null=True, blank=True)
    Subject = models.CharField(max_length=100, null=True, blank=True)
    Message = models.CharField(max_length=100, null=True, blank=True)
class CartDb(models.Model):
    Username = models.CharField(max_length=100, null=True, blank=True)
    Productname = models.CharField(max_length=100, null=True, blank=True)
    Quantity = models.IntegerField(null=True, blank=True)
    Total_Price = models.IntegerField(null=True, blank=True)
    Description = models.CharField(max_length=100, null=True, blank=True)
class Checkoutdb(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    FirstName=models.CharField(max_length=100,null=True,blank=True)
    LastName=models.CharField(max_length=100,null=True,blank=True)
    EmailId = models.CharField(max_length=100, null=True, blank=True)
    Address = models.CharField(max_length=100, null=True, blank=True)
    City=models.CharField(max_length=100,null=True,blank=True)
    Country=models.CharField(max_length=100,null=True,blank=True)
    Telephone=models.IntegerField(null=True,blank=True)
    cart=models.ForeignKey(CartDb,on_delete=models.CASCADE)
