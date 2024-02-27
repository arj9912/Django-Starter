from rest_framework import serializers
from products.models import Cart, CartItem, Category, Contact, Order, OrderItem, Product, Rating


class CustomRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.title
    
    def to_internal_value(self, data):
        return super().to_internal_value(data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title','image']


class RatingSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = ['rate','count']

    def get_rate(self,obj):
        product = Product.objects.filter(id=obj.product_id)
        all_rating = Rating.objects.filter(product=product)
        total_rating = 0
        for rating in all_rating:
            total_rating += rating.rate
        averate_rating = total_rating / all_rating.count()
        return averate_rating

    def get_count(self, obj):
        product = Product.objects.filter(id=obj.product_id)
        all_rating = Rating.objects.filter(product=product)
        count = all_rating.count()
        return count
    
 

class ProductSerializer(serializers.ModelSerializer):
    # rating = RatingSerializer()
    rating = serializers.SerializerMethodField()
    # categories = CategorySerializer(source="category", read_only=True)
    category = CategorySerializer(read_only=True)
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    class Meta:
        model = Product

        fields =['id','title','price','description', 'category','rating','image']


    def get_rating(self, obj):
        return {
            "rate": 0,
            "count": 0
        }


# class CreateProductSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Product

#         fields =['id','title','price','description', 'category','image']

class CreateProductSerializer(ProductSerializer):

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)

    class Meta(ProductSerializer.Meta):
        pass
    






class SimpleProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields  = ['id','title','price']



class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id','quantity','product','total_price']

    def get_total_price(self,cart_item):
        return cart_item.quantity * cart_item.product.price


class CreateCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields = ["product_id","quantity"]

    def create(self, validated_data):
        product_id = validated_data["product_id"]
        product = Product.objects.get(id=product_id)
        quantity = validated_data["quantity"]
        cart_id = self.context['cart_id']
        arjun = Cart.objects.get(id=cart_id)
        try:

            cart_item = CartItem.objects.get(cart=arjun, product=product)
            cart_item.quantity= cart_item.quantity + quantity
            cart_item.save()
        except CartItem.DoesNotExist:

            cart_item = CartItem.objects.create(cart=arjun, product=product, quantity=quantity)
        return cart_item


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']



class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items','total_price']

    def get_total_price(self,cart):
        return sum([item.product.price * item.quantity for item in cart.items.all()])



class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product','quantity']

    

class OrderSerializer(serializers.ModelSerializer):

    items=OrderItemSerializer(many=True, source='order_items',read_only=True)
    status=serializers.ReadOnlyField()
    cart_id=serializers.CharField(write_only=True)
    class Meta:
        model = Order
        fields = ["id", 'status', 'items','cart_id']

    
    def create(self, validated_data):
        cart_id= validated_data["cart_id"]
        cart=Cart.objects.get(id=cart_id)
        cart_items=cart.items.all()
        user=self.context["user"]
        order= Order.objects.create(customer=user)
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

        cart.delete()

        return order
    
            


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model= Contact
        fields = ['name', 'email', 'message']
