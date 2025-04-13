from django.db import models
from django.core.exceptions import ValidationError
import json
from django.http import JsonResponse


class Library(models.Model):
    nombre = models.CharField(max_length=30)
    direccion = models.TextField()
    telefono = models.CharField(max_length=9)
    
    

    def __str__(self):
        return f"{self.nombre} (id: {(self.id)})"

class User(models.Model):
    nombre = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    telefono = models.CharField(max_length=9)
    
    
    def __str__(self):
        return f"{self.nombre} {self.email} - {self.telefono} - {self.id}"

class Book(models.Model):
    titulo = models.CharField(max_length=40, blank=False, unique=True, null=False)
    autor = models.CharField(max_length=20)
    editorial = models.CharField(max_length=30)
    biblioteca = models.ForeignKey(Library, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titulo} (id: {self.id})"

class Loan(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    libro = models.ForeignKey(Book, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    devuelto = models.BooleanField(default=False)

    def __str__(self):
        return f"(Id:{self.id}) Préstamo de {self.libro} por {self.usuario.nombre} el dia: {self.fecha} ({'Devuelto' if self.devuelto else 'No devuelto'})"