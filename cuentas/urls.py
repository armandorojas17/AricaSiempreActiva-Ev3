from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('registro/', views.registrarView, name='registrar'),
    path('logout/', views.cerrar_sesion, name='logout'),
]