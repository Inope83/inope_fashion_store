from django.urls import path
from . import views

urlpatterns = [
    path('', views.produtu_list_view, name='produtu_list'),
    path('<int:pk>/', views.produtu_detail_view, name='produtu_detail'),
]
