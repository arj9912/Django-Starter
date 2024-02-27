from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from products.serializers import CartItemSerializer, CartSerializer, CategorySerializer, ContactSerializer, CreateCartItemSerializer, CreateProductSerializer, OrderSerializer, ProductSerializer, UpdateCartItemSerializer

from products.models import Cart, CartItem, Category, Contact, Order, Product
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from products.filters import ProductFilter


# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    # serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ["category__title", ]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateProductSerializer
        return ProductSerializer



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    



class CartViewSet(ModelViewSet):
    http_method_names = ['get','post','delete']
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete']

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs["cart_pk"])
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}


   
    
class OrderViewSet(ModelViewSet):
    http_method_names=["get","post","patch","option","head","delete"]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # def get_permissions(self):
    #     if self.action == "list":
    #         return [IsAdminUser()]
    #     return [IsAdminUSerOrAuthenticatedReadOnly()]


    # def get_serializer_class(self):
    #     if self.request.method=='PATCH':
    #         return UpdateOrderSerializer
    #     return OrderSerializer


    def get_serializer_context(self):
        return {'user':self.request.user}


class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
