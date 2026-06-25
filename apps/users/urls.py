from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('regist/', views.regist_view, name='regist'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('notifikasaun/', views.notifikasaun_list_view, name='notifikasaun_list'),
]
