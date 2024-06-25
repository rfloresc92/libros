from django.contrib import admin
from .models import Usuario, Contacto, Libro, Autores, Generos, Resena

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Contacto)
admin.site.register(Libro)
admin.site.register(Autores)
admin.site.register(Generos)
admin.site.register(Resena)