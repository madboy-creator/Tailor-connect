from django.db import models
from django.contrib.auth.models import User

class Producer(models.Model):
    name = models.CharField(max_length=200)
    contact_info = models.CharField(max_length=200)
    email = models.EmailField()
    location = models.CharField(max_length=200)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    prod_date = models.DateField()  # Production date
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    RARITY_CHOICES = [
        ('common', 'Common'),
        ('rare', 'Rare'),
        ('limited', 'Limited Edition'),
        ('unique', 'Unique Piece'),
    ]
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES, default='common')
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_info = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    
    def __str__(self):
        return self.user.username

class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer.user.username}"