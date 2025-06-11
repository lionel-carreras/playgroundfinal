from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib import messages


# login personalizado
class UserLoginView(LoginView):
   
    template_name = 'accounts/login.html'
    
    next_page = reverse_lazy('products:home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta creada correctamente. Ahora puedes iniciar sesión.")
            return redirect('accounts:login')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/registro.html', {'form': form})