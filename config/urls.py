from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.home_view, name='home'),
    path('home/', views.home_view),
    path('produtus/', include('apps.products.urls')),
    path('uzuarius/', include('apps.users.urls')),
    path('kareta/', include('apps.cart.urls')),
    path('pedidus/', include('apps.orders.urls')),
    path('dashboard/', include('apps.dashboard.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)