from django_filters import FilterSet
from store.models import Book

class BookFilter(FilterSet):
    class Meta : 
        model = Book
        fields = {
            'category_id' : ['exact'],
            'unit_price' : ['gt','lt']
        }