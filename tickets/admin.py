from django.contrib import admin
from tickets.models import Ticket, Asignacion, VerificarResolucion


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Ticket.
    """
    list_display = ['id', 'titulo', 'estado', 'prioridad', 'categoria', 'creado_por', 'fecha_creacion']
    list_filter = ['estado', 'prioridad', 'categoria']
    search_fields = ['titulo', 'descripcion']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Asignacion.
    """
    list_display = ['id', 'ticket', 'administrador', 'fecha_asignacion']
    list_filter = ['administrador']
    search_fields = ['ticket__titulo', 'administrador__nombre']


@admin.register(VerificarResolucion)
class VerificarResolucionAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo VerificarResolucion.
    """
    list_display = ['id', 'ticket', 'aceptada', 'fecha']
    list_filter = ['aceptada']