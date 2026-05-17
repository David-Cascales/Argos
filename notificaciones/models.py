from django.db import models
from django.conf import settings


class Notificacion(models.Model):
    """
    Representa un mensaje automático enviado por el sistema a un usuario cuando se produce un
    cambio relevante.
    """

    TIPOS = [
        ('ticket_creado', 'Ticket creado'),
        ('ticket_actualizado', 'Ticket actualizado'),
        ('ticket_asignado', 'Ticket asignado'),
        ('ticket_resuelto', 'Ticket resuelto'),
        ('ticket_eliminado', 'Ticket eliminado'),
        ('permiso_modificado', 'Permiso modificado'),
    ]

    mensaje = models.TextField()
    tipo = models.CharField(max_length=50, choices=TIPOS)
    leido = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notificaciones'
    )

    def enviar(self) -> None:
        """Marca la notificación como creada y lista para ser leída."""
        self.save()

    def marcar_leida(self) -> None:
        """Marca la notificación como leída."""
        self.leido = True
        self.save()

    def __str__(self) -> str:
        return f'[{self.tipo}] {self.usuario} - {self.fecha}'

    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha']