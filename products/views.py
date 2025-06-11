from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import ProfileForm, UserForm, ProductForm
from accounts.models import Profile
from django.contrib.auth import update_session_auth_hash


# raiz
def home(request):
    return render(request, 'home.html')

# Sobre Mí
def about(request):
    return render(request, 'about.html')

# Lista de productos
def comprar(request):
    productos = Product.objects.all()
    context = {'productos': productos}
    return render(request, 'comprar.html', context)

# Agregar producto al carrito
@login_required(login_url='accounts:login')
def add_to_cart(request, pk):
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1
    else:
        quantity = 1
    get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    key = str(pk)
    cart[key] = cart.get(key, 0) + quantity
    request.session['cart'] = cart
    return redirect('products:cart')


# listar productos carrito
@login_required(login_url='accounts:login')
def cart(request):
    cart_dict = request.session.get('cart', {})
    productos_carrito = []
    total = 0
    for pk_str, cantidad in cart_dict.items():
        try:
            producto = Product.objects.get(pk=int(pk_str))
        except Product.DoesNotExist:
            continue

        subtotal = producto.precio * cantidad
        total += subtotal

        productos_carrito.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })

    context = {
        'productos_carrito': productos_carrito,
        'total': total,
    }
    return render(request, 'cart.html', context)

def pago(request):
    return render(request, 'pago.html')

# Pagar con tarjeta simulada
@require_POST
def pagar(request):
    TARJETA_OK = 1234567890
    CVV_OK = '123'
    SALDO_DISPONIBLE = 2000000

    tarjeta = request.POST.get('card_number', '').replace(' ', '')
    cvv = request.POST.get('cvv', '')
    total = request.POST.get('total', '0')

    try:
        total = float(total)
    except ValueError:
        total = 0.0

    try:
        tarjeta = int(tarjeta)
    except ValueError:
        tarjeta = None

    if tarjeta == TARJETA_OK and cvv == CVV_OK and SALDO_DISPONIBLE >= total:
        messages.success(request, "Pago realizado. ¡Gracias por tu compra!")
        cantidades = request.session.get('cart', {})
        for pk_str, cantidad in cantidades.items():
            producto = get_object_or_404(Product, pk=int(pk_str))
            producto.stock -= cantidad
            producto.save()
        request.session.pop('cart', None)
        return redirect('products:comprar')
    else:
        messages.warning(request, "Pago rechazado: verifique su Tarjeta e intente nuevamente")
        return redirect('products:cart')

# Hacer una publicación de producto
@login_required(login_url='accounts:login')
def vender(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user
            producto.save()
            messages.success(request, "Producto publicado con éxito.")
            return redirect('products:comprar')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = ProductForm()
    return render(request, 'vender.html', {'form': form})

# Listar publicaciones del vendedor
@login_required(login_url='accounts:login')
def publicaciones(request):
    publicaciones = Product.objects.filter(vendedor_id=request.user.id)
    return render(request, 'vendedor/publicaciones.html', {'publicaciones': publicaciones})

# detalle del producto
@login_required(login_url='accounts:login')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, vendedor=request.user)
    return render(request, 'vendedor/product_detail.html', {
        'product': product
    })

# Editar producto
@login_required(login_url='accounts:login')
def product_edit(request, pk):  
    product = get_object_or_404(Product, pk=pk, vendedor=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('products:publicaciones')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = ProductForm(instance=product)

    return render(request, 'vendedor/product_edit.html', {
        'form': form,
        'product': product
    })

# Eliminar producto
@login_required(login_url='accounts:login')
def product_delete(request, pk):
    producto = get_object_or_404(Product, pk=pk, vendedor=request.user)
    producto.delete()
    messages.success(request, "Producto eliminado correctamente.")
    return redirect('products:publicaciones')

# Perfil del vendedor
@login_required(login_url='accounts:login')
def perfil(request):
    return render(request, 'vendedor/perfil.html')

# Editar perfil del vendedor
@login_required(login_url='accounts:login')
def edit_profile(request):
    user = request.user
    
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form    = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('products:perfil')
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        user_form    = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'vendedor/editar_perfil.html', {
        'user_form':    user_form,
        'profile_form': profile_form,
        'profile':      profile,
    })