from django.contrib.auth.models import User
from django.db import models

class Message(models.Model):
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    emisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emisor')
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receptor')

    def __str__(self):
        return f"De {self.emisor.username} a {self.receptor.username}: {self.contenido[:30]}"

