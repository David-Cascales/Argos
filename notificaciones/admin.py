from django.contrib import admin
from notificaciones.models import Notificacion


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'tipo', 'leido', 'fecha']
    list_filter = ['tipo', 'leido']
    search_fields = ['mensaje', 'usuario__nombre']
    ordering = ['-fecha']