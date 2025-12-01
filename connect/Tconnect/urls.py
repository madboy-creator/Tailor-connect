from django.urls import path, include
from . import views

urlpatterns = [
    # Main pages
    path('', views.landing_page, name='landing'),
    path('products/', views.products_list, name='products_list'),
    path('producers/', views.producers_list, name='producers_list'),
    
    # Product CRUD
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Producer CRUD
    path('producers/create/', views.producer_create, name='producer_create'),
    path('producers/<int:pk>/', views.producer_detail, name='producer_detail'),
    path('producers/<int:pk>/edit/', views.producer_update, name='producer_update'),
    path('producers/<int:pk>/delete/', views.producer_delete, name='producer_delete'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Orders
    path('order/<int:product_id>/', views.create_order, name='create_order'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),

     path('', include('django.contrib.auth.urls')),
]