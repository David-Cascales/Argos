from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from cuentas.models import Usuario, Rol


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Rol.
    """
    list_display = ['id', 'nombre', 'permisos']
    search_fields = ['nombre']


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuración del panel de administración para el modelo Usuario.
    Extiende UserAdmin para mantener la funcionalidad de gestión
    de contraseñas que Django proporciona por defecto.
    """
    list_display = ['id', 'nombre', 'email', 'rol', 'is_active', 'fecha_registro']
    list_filter = ['rol', 'is_active']
    search_fields = ['nombre', 'email']
    ordering = ['nombre']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('nombre', 'rol', 'activo')}),
        ('Permisos', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'rol', 'password1', 'password2'),
        }),
    )