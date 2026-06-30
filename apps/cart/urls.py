from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='kareta'),
    path('tau/', views.cart_add_view, name='karetatau'),
    path('hamos/<int:item_id>/', views.cart_remove_view, name='karetahamos'),
    path('atualiza/', views.cart_update_view, name='karetaatualiza'),
]
