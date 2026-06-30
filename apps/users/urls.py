from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='kliente_login'),
    path('registu/', views.regist_view, name='kliente_regist'),
    path('sai/', views.logout_view, name='kliente_logout'),
    path('sai-sistema/', views.django_logout_view, name='user_logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('perfil/edit/', views.perfil_view, name='perfil_edit'),
    path('notifikasaun/', views.notifikasaun_list_view, name='notifikasaun_list'),
]
