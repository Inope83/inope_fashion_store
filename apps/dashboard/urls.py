from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardHome.as_view(), name='dashboard_home'),
    path('report/', views.ReportView.as_view(), name='dashboard_report'),
    path('report/export/csv/', views.report_export_csv, name='dashboard_report_export'),

    # Kategoria
    path('kategoria/', views.KategoriaList.as_view(), name='kategoria_list'),
    path('kategoria/create/', views.KategoriaCreate.as_view(), name='kategoria_create'),
    path('kategoria/<pk>/update/', views.KategoriaUpdate.as_view(), name='kategoria_update'),
    path('kategoria/<pk>/delete/', views.KategoriaDelete.as_view(), name='kategoria_delete'),

    # Produtu
    path('produtu/', views.ProdutuList.as_view(), name='produtu_list'),
    path('produtu/create/', views.ProdutuCreate.as_view(), name='produtu_create'),
    path('produtu/<pk>/update/', views.ProdutuUpdate.as_view(), name='produtu_update'),
    path('produtu/<pk>/delete/', views.ProdutuDelete.as_view(), name='produtu_delete'),

    # Kliente
    path('kliente/', views.KlienteList.as_view(), name='kliente_list'),
    path('kliente/create/', views.KlienteCreate.as_view(), name='kliente_create'),
    path('kliente/<pk>/update/', views.KlienteUpdate.as_view(), name='kliente_update'),
    path('kliente/<pk>/delete/', views.KlienteDelete.as_view(), name='kliente_delete'),

    # Notifikasaun
    path('notifikasaun/', views.NotifikasaunList.as_view(), name='notifikasaun_list'),
    path('notifikasaun/create/', views.NotifikasaunCreate.as_view(), name='notifikasaun_create'),
    path('notifikasaun/<pk>/update/', views.NotifikasaunUpdate.as_view(), name='notifikasaun_update'),
    path('notifikasaun/<pk>/delete/', views.NotifikasaunDelete.as_view(), name='notifikasaun_delete'),

    # Pedidu
    path('pedidu/', views.PediduList.as_view(), name='pedidu_list'),
    path('pedidu/create/', views.PediduCreate.as_view(), name='pedidu_create'),
    path('pedidu/<pk>/update/', views.PediduUpdate.as_view(), name='pedidu_update'),
    path('pedidu/<pk>/delete/', views.PediduDelete.as_view(), name='pedidu_delete'),

    # DetalloPedidu
    path('detallu/', views.DetalloPediduList.as_view(), name='detallopedidu_list'),
    path('detallu/create/', views.DetalloPediduCreate.as_view(), name='detallopedidu_create'),
    path('detallu/<pk>/update/', views.DetalloPediduUpdate.as_view(), name='detallopedidu_update'),
    path('detallu/<pk>/delete/', views.DetalloPediduDelete.as_view(), name='detallopedidu_delete'),

    # Pagamentu
    path('pagamentu/', views.PagamentuList.as_view(), name='pagamentu_list'),
    path('pagamentu/create/', views.PagamentuCreate.as_view(), name='pagamentu_create'),
    path('pagamentu/<pk>/update/', views.PagamentuUpdate.as_view(), name='pagamentu_update'),
    path('pagamentu/<pk>/delete/', views.PagamentuDelete.as_view(), name='pagamentu_delete'),

    # Admin
    path('admin/', views.AdminList.as_view(), name='admin_list'),
    path('admin/create/', views.AdminCreate.as_view(), name='admin_create'),
    path('admin/<pk>/update/', views.AdminUpdate.as_view(), name='admin_update'),
    path('admin/<pk>/delete/', views.AdminDelete.as_view(), name='admin_delete'),
]
