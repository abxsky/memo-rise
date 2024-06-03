from django.urls import path
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('books', views.BookViewSet, basename='books')
router.register('categories', views.CategoryViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

books_router = routers.NestedDefaultRouter(router, 'books', lookup='book')
books_router.register('reviews', views.ReviewViewSet, basename='book-reviews')
books_router.register('images', views.BookImageViewSet, basename='book-images')

carts_router = routers.NestedDefaultRouter(router,'carts',lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + books_router.urls + carts_router.urls
#urlpattern = ['', include(router.urls)]