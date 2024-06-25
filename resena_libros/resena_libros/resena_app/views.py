from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroUsuarioForm, EmailAuthenticationForm, ContactoForm, FiltroLibrosForm, ResenaForm, AutoresForm, GenerosForm, LibroForm, AdminAuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Usuario, Libro, Resena
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
# Create your views here.
def inicio(request):
    return render(request,'inicio.html')

def registrate(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            #Crea user django
            user = User.objects.create_user(username=form.cleaned_data['email'], email=form.cleaned_data['email'], password=form.cleaned_data['contraseña'])
            #Crea instancia de usuario personalizado
            contraseña_hasheada = make_password(form.cleaned_data['contraseña'])
            usuario = Usuario.objects.create(
                user=user,
                nombre=form.cleaned_data['nombre'],
                email=form.cleaned_data['email'],
                contraseña = contraseña_hasheada,
                tipo_usuario='lector'
            )
            login(request, user)
            return redirect('../inicio/')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registrate.html', {'form': form})

class CustomLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    
class AdminLoginView(LoginView):
    authentication_form = AdminAuthenticationForm
    template_name = 'inicia_sesion_admin.html'
    
def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El formulario se ha enviado correctamente.')
            return redirect('contacto')
        else:
            messages.error(request, 'Ha ocurrido un error. Por favor, verifica los datos ingresados.')
    else:
        form = ContactoForm()
    storage = messages.get_messages(request)
    for message in storage:
        pass
    storage.used = True
    return render(request, 'contacto.html', {'form': form})

def libros(request):
    libros = Libro.objects.all()
    form = FiltroLibrosForm(request.GET)

    if form.is_valid():
        autor = form.cleaned_data.get('autor')
        genero = form.cleaned_data.get('genero')
        busqueda = form.cleaned_data.get('busqueda')

        if autor:
            libros = libros.filter(autor=autor)
        if genero:
            libros = libros.filter(genero=genero)
        if busqueda:
            libros = libros.filter(titulo__icontains=busqueda)

    return render(request, 'libros.html', {'form': form, 'libros': libros})

@login_required
def perfil(request):
    usuario = request.user.usuario
    return render(request, 'perfil.html', {'usuario': usuario})

@login_required
def crear_resena(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    
    if request.method == 'POST':
        form = ResenaForm(request.POST)
        if form.is_valid():
            resena = form.save(commit=False)
            resena.libro = libro
            resena.usuario = request.user.usuario
            resena.save()
            return redirect('detalle_libro', libro_id=libro_id)
    else:
        form = ResenaForm()
    reseñas = Resena.objects.filter(libro=libro)
    for reseña in reseñas:
        reseña.estrellas = ['★'] * reseña.calificacion
    return render(request, 'detalle_libro.html', {'libro': libro, 'reseñas': reseñas, 'form': form})

@login_required
def lista_usuarios(request):
    if not request.user.is_superuser:
        return redirect('inicio')

    usuarios = Usuario.objects.all().order_by('nombre')

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        nuevo_tipo = request.POST.get('nuevo_tipo')
        usuario = Usuario.objects.get(id=usuario_id)

        if nuevo_tipo != usuario.tipo_usuario:
            if nuevo_tipo == 'administrador':
                usuario.tipo_usuario = 'administrador'
                usuario.user.is_staff = True
                usuario.user.is_superuser = True
            else:
                usuario.tipo_usuario = 'lector'
                usuario.user.is_staff = False
                usuario.user.is_superuser = False

            usuario.save()
            usuario.user.save()

            return redirect('lista_usuarios')

    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

@login_required
def publicar_autor(request):
    if not request.user.is_superuser:
        return redirect('inicio')

    if request.method == 'POST':
        form = AutoresForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'El autor se ha publicado correctamente.')
                return redirect('publicar_autor')
            except IntegrityError:
                messages.error(request, 'El autor ya existe. Por favor, verifica los datos ingresados.')
        else:
            messages.error(request, 'Ha ocurrido un error. Por favor, verifica los datos ingresados.')
    else:
        form = AutoresForm()
    storage = messages.get_messages(request)
    for message in storage:
        pass
    storage.used = True
    return render(request, 'publicar_autor.html', {'form': form})

@login_required
def publicar_genero(request):
    if not request.user.is_superuser:
        return redirect('inicio')

    if request.method == 'POST':
        form = GenerosForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'El genero se ha publicado correctamente.')
                return redirect('publicar_genero')
            except IntegrityError:
                messages.error(request, 'El genero ya existe. Por favor, verifica los datos ingresados.')
        else:
            messages.error(request, 'Ha ocurrido un error. Por favor, verifica los datos ingresados.')
    else:
        form = GenerosForm()
    storage = messages.get_messages(request)
    for message in storage:
        pass
    storage.used = True
    return render(request, 'publicar_genero.html', {'form': form})

@login_required
def publicar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '¡El libro se ha publicado exitosamente!')
            return redirect('publicar_libro')
    else:
        form = LibroForm()
    storage = messages.get_messages(request)
    for message in storage:
        pass
    storage.used = True
    return render(request, 'publicar_libro.html', {'form': form})

@login_required
def detalle_libro_admin(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    reseñas = Resena.objects.filter(libro=libro)

    if request.method == 'POST':
        if 'eliminar_libro' in request.POST:
            libro.delete()
            messages.success(request, 'El libro ha sido eliminado correctamente.')
            return redirect('libros')
        elif 'eliminar_resena' in request.POST:
            resena_id = request.POST.get('resena_id')
            resena = get_object_or_404(Resena, id=resena_id)
            resena.delete()
            messages.success(request, 'La reseña ha sido eliminada correctamente.')
            return redirect(reverse('detalle_libro_admin', args=[libro_id]))

    for reseña in reseñas:
        reseña.estrellas = ['★'] * reseña.calificacion
    storage = messages.get_messages(request)
    for message in storage:
        pass
    storage.used = True
    return render(request, 'detalle_libro_admin.html', {'libro': libro, 'reseñas': reseñas})

@login_required
def mis_resenas(request):
    if request.method == 'POST' and 'eliminar_resena' in request.POST:
        resena_id = request.POST.get('resena_id')
        resena = get_object_or_404(Resena, id=resena_id, usuario=request.user.usuario)
        resena.delete()
        return redirect('mis_resenas')

    resenas = Resena.objects.filter(usuario=request.user.usuario)
    return render(request, 'mis_resenas.html', {'resenas': resenas})

@login_required
def editar_resena(request, resena_id):
    resena = get_object_or_404(Resena, id=resena_id, usuario=request.user.usuario)
    if request.method == 'POST':
        form = ResenaForm(request.POST, instance=resena)
        if form.is_valid():
            form.save()
            return redirect('mis_resenas')
    else:
        form = ResenaForm(instance=resena)
    return render(request, 'editar_resena.html', {'form': form})