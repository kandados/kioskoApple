# kioskoApp/models.py

from django.db import models

class Curiosidad(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fuente = models.URLField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
