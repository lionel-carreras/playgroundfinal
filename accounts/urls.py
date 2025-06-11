from django.urls import path
from .views import UserLoginView
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views

# urls de la app accounts que lleva login/registro/cambio de contraseña
app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('accounts:login')), name='logout'),
    path('register/', views.register, name='register'),
    path('password/change/',auth_views.PasswordChangeView.as_view(template_name='accounts/change_password.html',success_url='/perfil/'),name='password_change'),
]

