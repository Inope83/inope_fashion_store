from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/', views.cart_add_view, name='cart_add'),
    path('remove/<int:item_id>/', views.cart_remove_view, name='cart_remove'),
]
