from django.db import models


class Promotion(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()


class Category(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    slug = models.SlugField()
    inventory = models.DecimalField(max_digits=6, decimal_places=0)
    last_update = models.DateTimeField(auto_now= True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.DecimalField(decimal_places= 0, max_digits= 15)
    birth_date = models.DateField()
    

class Order(models.Model):

    #Order status constants
    ORDER_STATUS_PENDING = 'P'
    ORDER_STATUS_SENT = 'S'
    ORDER_STATUS_COMPLETED = 'C'
    ORDER_STATUS_FAILED =  'F'

    STATUS_CHOICES = {
        ORDER_STATUS_PENDING : 'Pending' ,
        ORDER_STATUS_SENT : 'Sent',
        ORDER_STATUS_COMPLETED : 'Completed',
        ORDER_STATUS_FAILED : 'Failed'
    }
    placed_at = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=STATUS_CHOICES, default=ORDER_STATUS_PENDING, max_length=1)
    user = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.DecimalField(max_digits=7, decimal_places=0, null=False, default='0')
    user = models.OneToOneField(Customer, on_delete=models.CASCADE,primary_key= True)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()