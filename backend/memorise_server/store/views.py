from http import HTTPStatus

from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .models import OrderItem
from .permissions import IsAdminOrReadOnly, ViewCustomerHistoryPermission
from .pagination import DefaultPagination
from .filters import BookFilter
from .serializers import *

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all() 
    serializer_class = BookSerializer

    #permissions
    permission_classes = [IsAdminOrReadOnly]
    
    #filters and sorting
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    #pagination
    pagination_class = DefaultPagination
    
    def get_serializer_context(self):
         return {'request':self.request}

    def delete(self,request,pk):
         book = get_object_or_404(Book,pk=pk)
         if book.objects.orderitems.count() > 0 :
              return Response({'error': "Ne peut pas supprimer un produit qui a des articles associés"}, 
                status=status.HTTP_204_NO_CONTENT)
         
class CategoryViewSet(ModelViewSet):
     queryset = Category.objects.annotate(book_count = Count('book')).all()
     serializer_class = CategorySerializer
     permission_classes = [IsAdminOrReadOnly]
     
     def get_serializer_context(self):
          return super().get_serializer_context()
     
     def destroy(self, request, *args, **kwargs):
          if OrderItem.objects.filter(book_id= kwargs['id']).count() > 0:
               {'error':'le livre ne peut pas étre supprimer car il a des articles d\' une ou plusieurs commandes qui lui sont associés'}
          return super().destroy(request, *args, **kwargs)
        
class ReviewViewSet(ModelViewSet):
     serializer_class = ReviewSerializer

     #getting the book_pk so it becomes usable in the serializer
     def get_serializer_context(self):
          return {'book_id': self.kwargs['book_pk']}
     
     #filtering book-specific reviws
     def get_queryset(self):
          return Review.objects.filter(book_id = self.kwargs['book_pk'])

class CartViewSet(CreateModelMixin,
               RetrieveModelMixin,
               DestroyModelMixin,
               GenericViewSet):
     queryset = Cart.objects.prefetch_related('cartitem_set__book').all()
     serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
     http_method_names = ['get', 'post', 'patch', 'delete']
     def get_serializer_class(self):
          if self.request.method == 'POST':
               return AddCartItemSerializer
          elif self.request.method == 'PATCH':
               return UpdateCartItemSerializer
          return CartItemSerializer
     
     def get_serializer_context(self):
          return {'cart_id':self.kwargs['cart_pk']}

     def get_queryset(self):
          return CartItem.objects.filter(cart_id = self.kwargs['cart_pk']).\
               select_related('book')

class CustomerViewSet(ModelViewSet):
     queryset = Customer.objects.all()
     serializer_class = CustomerSerializer
     permission_classes = [IsAdminUser]

     @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
     def history(self, request, pk):
          return(Response('ok'))
     
     @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
     def me(self, request):
          if request.method == 'GET':
               customer = Customer.objects.get(user_id = request.user.id)
               serializer = CustomerSerializer(customer)
               return Response(serializer.data)
          elif request.method == 'PUT' : 
               serializer = CustomerSerializer(customer, data=request.data, partial = True)
               serializer.is_valid(raise_exception=True)
               serializer.save()
               return Response(serializer.data)
          
class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        customer_id = Customer.objects.only(
            'id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)
    
class BookImageViewSet(ModelViewSet):
     serializer_class = BookImageSerializer
     
     def get_serializer_context(self):
          return {'book_id': self.kwargs['book_pk']}
     def get_queryset(self):
          return BookImage.objects.filter(book_id=self.kwargs['book_pk'])