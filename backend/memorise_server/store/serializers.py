from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import *
from .signals import order_created


class BookImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        book_id = self.context['book_id']
        return BookImage.objects.create(book_id = book_id, **validated_data)
    class Meta:
        model = BookImage
        fields = ['id', 'image']

class BookSerializer(serializers.ModelSerializer):
    bookimage_set = BookImageSerializer(many=True, read_only=True)
    class Meta: 
        model = Book
        fields = ['id', 'title', 'unit_price','price_with_tax','category', 'inventory', 'description', 'bookimage_set']
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, book:Book):
        return book.unit_price * Decimal('1.1')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title' ]
    # book_count = serializers.IntegerField(read_only=True)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','created_at', 'name', 'description']

    def create(self, validated_data):
        book_id = self.context['book_id']
        # validated_data['book_id'] = book_id
        return Review.objects.create(book_id = book_id, **validated_data)

class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item:CartItem):
        return cart_item.quantity * (cart_item.book.unit_price)
    
    class Meta:
        model = CartItem
        fields = ['cart', 'book', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    cartitem_set = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum(item.quantity * item.book.unit_price for item in cart.cartitem_set.all())
    
    class Meta:
        model = Cart
        fields = ['id', 'cartitem_set', 'total_price']

#TODO
class AddCartItemSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField()
    
    def validate_book_id(self, value):
        if not Book.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Aucun livre qui a cet id trouvé')
        return value

    def save(self):
        cart_id = self.context['cart_id']
        book_id = self.validated_data['book_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id = cart_id, book_id = book_id, )
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id = cart_id, **self.validated_data)
        return self.instance
    
    class Meta:
        model = CartItem
        fields = ['id', 'book_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date']


class OrderItemSerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'book', 'unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'status', 'orderitem_set']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('Aucun Panier avec cet id trouvé')
        if CartItem.objects.filter(cart_id = cart_id).count() == 0:
            raise serializers.ValidationError('Le panier est vide')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            customer = Customer.objects.get(user_id = self.context['user_id'])
            order = Order.objects.create(customer = customer)
            cart_items = CartItem.objects.select_related('book').filter(cart_id = self.validated_data['cart_id'])
            order_items = [
                OrderItem(
                order = order,
                book = item.book,
                unit_price = item.book.unit_price,
                quantit = item.quantity
            ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete()
            order_created.send_robust(self.__class__, order=order)
            return order

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

