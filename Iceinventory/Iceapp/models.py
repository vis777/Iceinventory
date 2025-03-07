from django.db import models
from django.contrib.auth.models import User
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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ice_stock = models.ForeignKey('Shopapp.IceStock', on_delete=models.CASCADE)  # Lazy import using string
    quantity_ordered = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    status_choices = [
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled')
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')



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
    FirstName=models.CharField(max_length=100,null=True,blank=True)
    LastName=models.CharField(max_length=100,null=True,blank=True)
    EmailId = models.CharField(max_length=100, null=True, blank=True)
    Address = models.CharField(max_length=100, null=True, blank=True)
    City=models.CharField(max_length=100,null=True,blank=True)
    Country=models.CharField(max_length=100,null=True,blank=True)
    Telephone=models.IntegerField(null=True,blank=True)
