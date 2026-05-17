from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class Rol(models.Model):
    """
    Representa el rol de un usuario en el sistema.
    Define los permisos y capacidades de cada perfil de usuario.
    """
    nombre = models.CharField(max_length=50, unique=True)
    permisos = models.TextField(blank=True)

    def asignar_permiso(self, permiso: str) -> None:
        permisos_lista = self.permisos.split(',') if self.permisos else []
        if permiso not in permisos_lista:
            permisos_lista.append(permiso)
            self.permisos = ','.join(permisos_lista)
            self.save()

    def revocar_permiso(self, permiso: str) -> None:
        permisos_lista = self.permisos.split(',') if self.permisos else []
        if permiso in permisos_lista:
            permisos_lista.remove(permiso)
            self.permisos = ','.join(permisos_lista)
            self.save()

    def __str__(self) -> str:
        return self.nombre

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'


class UsuarioManager(BaseUserManager):
    """
    Manager personalizado para el modelo Usuario.
    Se aplica el patrón Factory Strategy: centraliza la creación de instancias de Usuario.
    """

    def create_user(self, email: str = None, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        nombre = extra_fields.pop('nombre', email.split('@')[0])
        user = self.model(email=email, nombre=nombre, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str = None, nombre: str = '', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if not nombre:
            nombre = email.split('@')[0]
        return self.create_user(email, password, nombre=nombre, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario personalizado.
    Esta clase es el eje central del sistema, tal como se describe en el diagrama de clases
    del análisis UML del proyecto.
    """
    nombre = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    rol = models.ForeignKey(
        Rol,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios'
    )
    # activo = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    fecha_registro = models.DateTimeField(auto_now_add=True)

    # Campos requeridos por Django
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def iniciar_sesion(self) -> None:
        """Lógica de inicio de sesión delegada a Django Auth."""
        pass

    def cerrar_sesion(self) -> None:
        """Lógica de cierre de sesión delegada a Django Auth."""
        pass

    def __str__(self) -> str:
        return f'{self.nombre} ({self.email})'

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'