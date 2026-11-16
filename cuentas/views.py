from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from .models import Rol, Perfil


def registro_usuario(request):

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        rol = request.POST.get('rol', '')

        if not username or not email or not password:
            messages.error(request, 'Completa todos los campos obligatorios.')
            return redirect('registro')

        if rol not in ['turista', 'gremio']:
            messages.error(request, 'Selecciona un tipo de cuenta válido.')
            return redirect('registro')

        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('registro')

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, 'Ese nombre de usuario ya existe.')
            return redirect('registro')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'Ese correo ya está registrado.')
            return redirect('registro')

        try:
            validate_password(password)
        except ValidationError as error:
            for mensaje in error.messages:
                messages.error(request, mensaje)

            return redirect('registro')

        usuario = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        nombre_rol = 'Gremio' if rol == 'gremio' else 'Turista'
        rol_objeto, creado = Rol.objects.get_or_create(nombre=nombre_rol)

        Perfil.objects.create(
            usuario=usuario,
            rol=rol_objeto
        )

        login(request, usuario)

        if rol == 'gremio':
            return redirect('panel_gremio')

        return redirect('panel_turista')

    return render(request, 'cuentas/registro.html')


def login_usuario(request):

    if request.method == 'POST':

        identificador = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        usuario_registrado = None

        if '@' in identificador:
            usuario_registrado = User.objects.filter(
                email__iexact=identificador
            ).first()
        else:
            usuario_registrado = User.objects.filter(
                username__iexact=identificador
            ).first()

        usuario = None

        if usuario_registrado:
            usuario = authenticate(
                request,
                username=usuario_registrado.username,
                password=password
            )

        if usuario is not None:

            login(request, usuario)

            if usuario.is_superuser:
                return redirect('/admin/')

            rol_turista, creado = Rol.objects.get_or_create(
                nombre='Turista'
            )

            perfil, creado = Perfil.objects.get_or_create(
                usuario=usuario,
                defaults={'rol': rol_turista}
            )

            nombre_rol = perfil.rol.nombre.lower()

            if nombre_rol == 'moderador':
                return redirect('panel_moderador')

            elif nombre_rol == 'gremio':
                return redirect('listar_gremio')

            else:
                return redirect('panel_turista')

        messages.error(
            request,
            'Nombre de usuario, correo o contraseña incorrectos.'
        )

    return render(request, 'cuentas/login.html')


def cerrar_sesion(request):

    logout(request)

    return redirect('/')


@login_required
def panel_moderador(request):

    if not hasattr(request.user, 'perfil'):
        return redirect('/')

    if request.user.perfil.rol.nombre.lower() != 'moderador':
        return redirect('/')

    return render(request, 'cuentas/panel_moderador.html')


@login_required
def panel_gremio(request):

    if not hasattr(request.user, 'perfil'):
        return redirect('/')

    if request.user.perfil.rol.nombre.lower() != 'gremio':
        return redirect('/')

    return render(request, 'cuentas/panel_gremio.html')


@login_required
def panel_turista(request):

    if not hasattr(request.user, 'perfil'):
        return redirect('/')

    if request.user.perfil.rol.nombre.lower() != 'turista':
        return redirect('/')

    return render(request, 'cuentas/panel_turista.html')