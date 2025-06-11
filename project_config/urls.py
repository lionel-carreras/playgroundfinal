
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings

# urls del panel admin e inclusión de las apps
urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('products.urls')),
    path('messenger/', include(('messenger.urls','messenger'), namespace='messenger')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

