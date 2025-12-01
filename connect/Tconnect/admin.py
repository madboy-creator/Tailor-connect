from django.contrib import admin
from .models import Producer, Product, Customer, Order

@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'location', 'created_at']
    list_filter = ['location', 'created_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'producer', 'price', 'rarity', 'prod_date', 'image_preview']
    list_filter = ['rarity', 'prod_date']
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="width: 50px; height: 50px; object-fit: cover;" />'
        return "No image"
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'contact_info', 'location']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'product', 'quantity', 'status', 'order_date']
    list_filter = ['status', 'order_date']