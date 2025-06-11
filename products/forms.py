from django import forms
from .models import Product
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from accounts.models import Profile



class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name  = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email      = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model  = User
        fields = ['first_name','last_name','email']

class ProfileForm(forms.ModelForm):
    avatar    = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
    biografia = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':3}))

    class Meta:
        model  = Profile
        fields = ['avatar','biografia']


class ProductForm(forms.ModelForm):
    descripcion = forms.CharField(widget=CKEditorWidget(), label="Descripción")
    
    class Meta:
        model = Product
        fields = ['titulo', 'descripcion', 'categoria', 'precio', 'stock', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control'}),
            'categoria': forms.Select(attrs={'class':'form-select'}),
            'precio': forms.NumberInput(attrs={'class':'form-control', 'step':'0.01'}),
            'stock': forms.NumberInput(attrs={'class':'form-control', 'min':'1'}),
            'imagen': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }