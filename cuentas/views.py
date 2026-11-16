
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import PerfilForm
from .models import Perfil
from django.contrib.auth import login, logout
from django.contrib import messages


from django.contrib.auth.decorators import login_required

def registrarView(request):
    
    form = PerfilForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado')
            return redirect('login')

    return render(request, 'cuentas/registro.html', {'form':form})


def loginView(request):
    if request.user.is_authenticated:
        return redirect ('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            perfil,_=Perfil.objects.get_or_create(user=user)
            login(request, user)
            return redirect('listar_gremio')
        
    else:
        form = AuthenticationForm()
    return render(request, 'cuentas/login.html', {'form':form})
    


def cerrar_sesion(request):

    logout(request)

    return redirect('/')




@login_required
def panel_moderador(request):

    if not hasattr(request.user, 'perfil'):
        return redirect('/')

    if request.user.perfil.rol != 'moderador':
        return redirect('/')

    return render(request, 'cuentas/panel_moderador.html')



@login_required
def panel_gremio(request):

    if not hasattr(request.user, 'perfil'):
        return redirect('/')

    if request.user.perfil.rol != 'gremio':
        return redirect('/')

    return render(request, 'cuentas/panel_gremio.html')



@login_required
def panel_turista(request):

    if not hasattr(request.user, 'perfil'):
        return redirect('/')

    if request.user.perfil.rol != 'turista':
        return redirect('/')

    return render(request, 'cuentas/panel_turista.html')
