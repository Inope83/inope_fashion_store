
from django.urls import include, path

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('core.urls')),
] 
