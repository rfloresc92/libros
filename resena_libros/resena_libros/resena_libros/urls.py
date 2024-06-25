"""
URL configuration for resena_libros project.

The `urlpatterns` list routes URLs to  For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from resena_app.views import *
from django.contrib.auth.views import LogoutView, LoginView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', inicio, name='inicio'),
    path('inicia_sesion/', CustomLoginView.as_view(template_name='inicia_sesion.html'), name='inicia_sesion'),
    path('inicia_sesion_admin/', LoginView.as_view(template_name='inicia_sesion_admin.html'), name='inicia_sesion_admin'),
    path('registrate/', registrate, name='registrate'),
    path('logout/', LogoutView.as_view(template_name='inicio.html'), name='logout'),
    path('contacto/', contacto, name='contacto'),
    path('libros/', libros, name='libros'),
    path('perfil/', perfil, name='perfil'),
    path('usuarios/', lista_usuarios, name='lista_usuarios'),
    path('publicar_autor/', publicar_autor, name='publicar_autor'),
    path('publicar_genero/', publicar_genero, name='publicar_genero'),
    path('publicar_libro/', publicar_libro, name='publicar_libro'),
    path('libros/<int:libro_id>/', crear_resena, name='detalle_libro'),
    path('libro/<int:libro_id>/', detalle_libro_admin, name='detalle_libro_admin'),
    path('mis_resenas/', mis_resenas, name='mis_resenas'),
    path('editar_resena/<int:resena_id>/', editar_resena, name='editar_resena'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
