from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.produtu_detail_view, name='produtu_detail'),
]
