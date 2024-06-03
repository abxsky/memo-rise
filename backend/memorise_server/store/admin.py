from typing import Any
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.db.models import Count
from django.utils.html import format_html
from urllib.parse import urlencode
from django.urls import reverse

from .models import *

class BookImageInline(admin.TabularInline):
    model = BookImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail" />')
        return ''

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [BookImageInline]

    list_filter = ['category', 'last_update']
    list_display = ['title', 'unit_price', 'inventory_status', 'category', 'author']
    list_select_related= ['category','author']
    list_editable = ['unit_price']
    list_per_page = 10
    
    autocomplete_fields = ['category']
    search_fields = ['title__istartswith', 'category__title__istartswith', 'author__name__istartswith']
    prepopulated_fields = {
        'slug':['title']
    }

    @admin.display(ordering='inventory')
    def inventory_status(self,book ):
        if(book.inventory == 0):
            return 'Vide'
        elif(book.inventory < 50):
            return 'Bas'
        elif(book.inventory <= 100 and book.inventory >= 50 ):
            return 'Moyen'
        else:
            return 'Complet'
    inventory_status.short_description = 'inventaire'
    class Media:
        css = {
            'all': ['./store/style.css']
        }

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name',]
    search_fields = ['name']
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','phone' ,'order_count']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith','last_name__istartswith', 'phone__startswith']
    list_per_page = 10
    list_select_related = ['user']

    @admin.display(ordering='order_count')
    def order_count(self, customer):
        url = reverse('admin:store_order_changelist') + '?' + urlencode({ 
            'customer__id' : str(customer.id) })
        return format_html('<a href="{}">{}</a>', url, customer.order_count)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(order_count = Count('order'))
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'book_count']
    search_fields = ['title__istartswith']
    @admin.display(ordering='book_count')
    
    def book_count(self, category):
        url = reverse('admin:store_book_changelist') + '?' + urlencode({
            'category__id' : str(category.id)
        })
        
        return format_html('<a href="{}">{}</a>',url, category.book_count)
    
    book_count.short_description = 'Nombre de livres' 

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(book_count = Count('book'))
    
class OrderItemInLine(admin.TabularInline):
    min_num = 1
    max_num = 20
    model = OrderItem
    autocomplete_fields = ['book']
    extra = 0
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'customer_name', 'customer_phone', 'placed_at']
    list_select_related = ['customer']
    search_fields = ['customer__first_name__istartswith', 'customer__last_name__istartswith', 'customer__phone__istartswith']
    inlines = [OrderItemInLine]
    
    
    def customer_name(self, order):
        return order.customer
    
    customer_name.short_description = 'Client'

    def customer_phone(self,order):
        return order.customer.phone
    
    customer_phone.short_description = 'telephone'
    

