from django.db import models
from django.contrib.auth.models import User


def rol_defecto():
    rol, creado = Rol.objects.get_or_create(nombre='Turista')
    return rol.id


class Rol(models.Model):

    nombre = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nombre


class Perfil(models.Model):

    rol = models.ForeignKey(
        Rol,
        on_delete=models.RESTRICT,
        default=rol_defecto
    )

    foto_perfil = models.ImageField(
        upload_to='perfil',
        null=True,
        blank=True
    )

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil'
    )

    def __str__(self):
        return '{} - {}'.format(
            self.usuario.username,
            self.rol.nombre
        )



class PerfilUsuario(models.Model):

    ROLES = [
        ('turista', 'Turista'),
        ('gremio', 'Gremio'),
        ('moderador', 'Moderador'),
    ]

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil_anterior'
    )

    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default='turista'
    )

    def __str__(self):
        return '{} - {}'.format(
            self.usuario.username,
            self.get_rol_display()
        )