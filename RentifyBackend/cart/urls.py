from django.urls import path
from .views import CartDetailView, AddCartItemView, RemoveCartItemView

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart-detail'),
    path('add/', AddCartItemView.as_view(), name='add-to-cart'),
    path('remove/', RemoveCartItemView.as_view(), name='remove-from-cart'),
]
