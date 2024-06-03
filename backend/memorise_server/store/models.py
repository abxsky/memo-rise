from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.contrib import admin
from uuid import uuid4
from .validators import *

class Author(models.Model):
    def __str__(self) -> str:
        return self.name

    name = models.CharField(max_length=255, verbose_name='nom')
    biography = models.TextField(verbose_name='biographie', blank=True)

    class Meta:
        verbose_name = 'auteur'
        verbose_name_plural = 'auteurs'

class Address(models.Model):
    street = models.CharField(max_length=255, verbose_name='rue')
    city = models.CharField(max_length=255, verbose_name='ville')
    zip_code = models.DecimalField(max_digits=7, decimal_places=0, null=False, default='0', verbose_name='code postal')
    customer = models.OneToOneField('Customer', on_delete=models.CASCADE,primary_key= True, verbose_name='client')
    class Meta:
        verbose_name = 'Adresse'
        verbose_name_plural = 'Adresses'

class Book(models.Model):
    def __str__(self) -> str:
        return self.title

    title = models.CharField(max_length=255, verbose_name='titre')
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='prix unitaire', validators=[MinValueValidator(Decimal(1))])
    slug = models.SlugField()
    inventory = models.DecimalField(max_digits=6, decimal_places=0, verbose_name='inventaire',validators=[MinValueValidator(Decimal(1))])
    last_update = models.DateTimeField(auto_now= True, verbose_name='dernier mise a jour')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='categorie')
    promotions = models.ManyToManyField('Promotion',blank=True, verbose_name='promotions')
    author = models.ForeignKey('Author', on_delete=models.CASCADE,verbose_name='auteur')
    class Meta:
        verbose_name = "Livre"
        verbose_name_plural = "Livres"

class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/images', validators=[validate_file_size])

class CartItem(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, verbose_name='livre')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name='panier')
    quantity = models.PositiveSmallIntegerField(verbose_name='quantité', validators=[MinValueValidator(Decimal(1)), MaxValueValidator(Decimal(99))])  
    class Meta:
        unique_together = [['cart', 'book']]
        verbose_name = 'Article Chariot'
        verbose_name_plural = 'Articles Chariot'

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='crée le')
    class Meta:
        verbose_name = 'Panier'
        verbose_name_plural = 'Paniers'

class Category(models.Model): 
    def __str__(self) -> str:
        return self.title

    title = models.CharField(max_length=255, verbose_name='titre')
    featured_book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name='livre en vedette') 
    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categories"

class Customer(models.Model):
    def __str__(self) -> str:
        return self.user.first_name + ' ' + self.user.last_name
    
    phone = models.DecimalField(null=True, blank=True, decimal_places = 0, max_digits= 15, default=0, verbose_name='téléphone')
    birth_date = models.DateField(null=True, blank=True, verbose_name='date de naissance')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    class Meta:
        permissions = [
            ('view_history','Can view history')
            ]
        ordering = ['user__first_name', 'user__last_name']
        verbose_name = "Client"
        verbose_name_plural = "Clients"


class OrderItem(models.Model):
    order = models.ForeignKey('Order',on_delete=models.PROTECT, verbose_name='commande')
    book = models.ForeignKey('Book', on_delete=models.PROTECT, verbose_name='livre')
    quantity = models.PositiveSmallIntegerField(verbose_name='quantité')
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='prix unitaire')
    class Meta:
        verbose_name = 'Article Commande'
        verbose_name_plural = 'Articles Commande'

class Order(models.Model):
    #Order status constants
    ORDER_STATUS_PENDING = 'P'
    ORDER_STATUS_SENT = 'S'
    ORDER_STATUS_COMPLETED = 'C'
    ORDER_STATUS_FAILED =  'F'

    STATUS_CHOICES = {
        ORDER_STATUS_PENDING : 'En Attente' ,
        ORDER_STATUS_SENT : 'Envoyée',
        ORDER_STATUS_COMPLETED : 'Livrée',
        ORDER_STATUS_FAILED : 'Échoué'
    }

    placed_at = models.DateTimeField(auto_now_add=True, verbose_name='passé le')
    status = models.CharField(choices=STATUS_CHOICES, default=ORDER_STATUS_PENDING, max_length=1, verbose_name='état')
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT, verbose_name='client')
    
    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"


class Promotion(models.Model):
    title = models.CharField(max_length=255, verbose_name='titre')
    description = models.TextField()
    
    class Meta:
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"

class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='nom' )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
