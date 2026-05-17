from django.contrib import admin
from inventario.models import ItemInventario


@admin.register(ItemInventario)
class ItemInventarioAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo ItemInventario.
    """
    list_display = ['id', 'nombre', 'tipo', 'estado', 'gestionado_por', 'fecha_registro']
    list_filter = ['tipo', 'estado']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']