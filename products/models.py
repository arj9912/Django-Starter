from uuid import uuid4
from django.db import models

from django.contrib.auth.models import User


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100)
    featured_product = models.ForeignKey("Product",on_delete=models.SET_NULL,null=True,blank=True, related_name="categories")
    image = models.ImageField(upload_to='images/category')

    def __str__(self) -> str:
        return self.title


class Rating(models.Model):
    rate = models.DecimalField(max_digits=5 ,decimal_places=1)
    review = models.TextField(blank=True,null=True)
    product = models.ForeignKey("Product",on_delete=models.CASCADE)
    

    def __str__(self) -> str:
        return self.review

class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    # rating = models.ForeignKey(Rating, on_delete=models.CASCADE,null= True, blank=True)
    image = models.ImageField(upload_to='images/product')
    


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE)



ODER_STATUS_PENDING ='p'
ODER_STATUS_COMPLETE ='c'
ODER_STATUS_FAILED ='f'

ODER_STATUS_CHOICES = [
    (ODER_STATUS_PENDING,"Pending"),
    (ODER_STATUS_COMPLETE,"Complete"),
    (ODER_STATUS_FAILED,"failed"),
]


class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.PROTECT)
    placed_at = models.DateTimeField(auto_now_add=True)
    status =  models.CharField(max_length=1, default=ODER_STATUS_PENDING, choices=ODER_STATUS_CHOICES)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity= models.PositiveIntegerField()


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField(blank=True, null=True)