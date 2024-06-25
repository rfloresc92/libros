from django import forms
from .models import Usuario, Contacto, Autores, Generos, Resena, Libro
from django.contrib.auth.forms import AuthenticationForm

class RegistroUsuarioForm(forms.ModelForm):
    contraseña = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['nombre','email','contraseña']
        
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Correo electrónico")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': True})

class AdminAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': True})
        
class ContactoForm(forms.ModelForm):
    class Meta:
        model= Contacto
        fields=['nombre','email','mensaje']
        
class FiltroLibrosForm(forms.Form):
    autor = forms.ModelChoiceField(queryset=Autores.objects.all(), empty_label="Todos los autores", required=False)
    genero = forms.ModelChoiceField(queryset=Generos.objects.all(), empty_label="Todos los géneros", required=False)
    busqueda = forms.CharField(max_length=100, required=False)    
    
class ResenaForm(forms.ModelForm):
    calificacion = forms.ChoiceField(
        choices=[(i, '★' * i) for i in range(1, 6)],
        widget=forms.RadioSelect
    )

    class Meta:
        model = Resena
        fields = ['comentario', 'calificacion']
        exclude = ['libro'] 
        

class AutoresForm(forms.ModelForm):
    class Meta:
        model = Autores
        fields = ['nombre','apellido']
        
class GenerosForm(forms.ModelForm):
    class Meta:
        model = Generos
        fields = ['nombre']
        
class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'descripcion', 'año_publicacion', 'portada', 'genero', 'autor']
        
    def __init__(self, *args, **kwargs):
        super(LibroForm, self).__init__(*args, **kwargs)
        self.fields['genero'].queryset = Generos.objects.all()
        self.fields['autor'].queryset = Autores.objects.all()