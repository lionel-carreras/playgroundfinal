from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField



class Category(models.Model):
    nombre = models.CharField(max_length=255)
    

    def __str__(self):
        return self.nombre



class Product(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = RichTextField(max_length=255)
    categoria = models.ForeignKey('Category', on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='products/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=1)
    


    def __str__(self):
        return (f"{self.titulo} - {self.categoria.nombre} - {self.descripcion} - ${self.precio}"
        )