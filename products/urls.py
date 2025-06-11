
from django.contrib import admin
from django.urls import path
from . import views
from django.urls import include

# Todas las urls del proyecto a excepción de panel admin, mensajes y login estan acá
app_name = 'products' 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('comprar/', views.comprar, name='comprar'),
    path('vender/', views.vender, name='vender'),
    path('cart/', views.cart, name='cart'),
    path('add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('', include('accounts.urls'), name='accounts'),
    path('pago/', views.pago, name='pago'),
    path('pagar/', views.pagar, name='pagar'),
    path('vender/', views.vender, name='vender'),
    path('publicaciones/', views.publicaciones, name='publicaciones'),
    path('<int:pk>/', views.product_detail, name='detail'),
    path('<int:pk>/edit/', views.product_edit, name='edit'),
    path('<int:pk>/delete/', views.product_delete, name='delete'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/edit/', views.edit_profile, name='edit_profile'),
    
   
]
