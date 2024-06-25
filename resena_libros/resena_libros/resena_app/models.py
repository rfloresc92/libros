from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Usuario(models.Model):
    TIPO = (
        ('administrador', 'Administrador'),
        ('lector', 'Lector'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=100)
    tipo_usuario = models.CharField(max_length=50, default='lector', choices=TIPO)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'contraseña']
    
    class Meta:
        db_table='usuario'
    
    def __str__(self) -> str:
        return f"{self.nombre} {self.email} {self.tipo_usuario}"
    
class Contacto(models.Model):
    nombre = models.CharField(max_length=30)
    email = models.EmailField()
    mensaje = models.TextField()
    class Meta:
        db_table='contacto'

class Generos(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    class Meta:
        db_table='genero'
    def __str__(self) -> str:
        return f"{self.nombre}"
    
class Autores(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    class Meta:
        db_table='autores'
        unique_together = ('nombre', 'apellido')
    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido}"
    

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    año_publicacion = models.IntegerField()
    portada = models.ImageField(upload_to='resena_app/media/libros/', null=True, blank=True)
    genero = models.ForeignKey(Generos, on_delete=models.CASCADE)
    autor = models.ForeignKey(Autores, on_delete=models.CASCADE)
    class Meta:
        db_table='libro'
    def __str__(self):
        return f"{self.titulo} ({self.autor}) - {self.año_publicacion}"
    
class Resena(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    calificacion = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField()
    fecha_reseña = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='resena'

    def __str__(self):
        return f"Reseña de {self.usuario} sobre {self.libro}"