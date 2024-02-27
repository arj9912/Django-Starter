from django.urls import path

from. import views


from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

router = DefaultRouter()

router.register('products', views.ProductViewSet, basename='products')
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('carts', views.CartViewSet, basename='carts')
router.register('orders', views.OrderViewSet, basename='orders')
router.register('contacts', views.ContactViewSet, basename='contacts')

cart_router = NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = [

    # path('product',views.product),
]



urlpatterns = urlpatterns + router.urls + cart_router.urls 