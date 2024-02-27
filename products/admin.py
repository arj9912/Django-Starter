from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from products.models import Cart, CartItem, Category, Contact, Order, OrderItem, Product, Rating

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display =['id','title','featured_product','image']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['rate','review']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','price','description','category','image']
    


class CartItemInlineAdmin(admin.TabularInline):
    model = CartItem
    extra =2
    max_num=3
    min_num =1
    

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=("id","modified_at","created_at")
    inlines= (CartItemInlineAdmin,)


class OrderItemInlineAdmin(admin.TabularInline):
    model = OrderItem
    extra= 2
    max_num=3
    min_num=1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=("id",)
    inlines=(OrderItemInlineAdmin,)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display=("name", "email", "message")
    
