from django.db import models
from django.conf import settings


class Ticket(models.Model):
    """
    Registra y documenta una incidencia.
    """

    ESTADOS = [
        ('abierto', 'Abierto'),
        ('en_progreso', 'En progreso'),
        ('pendiente', 'Pendiente'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado'),
    ]

    PRIORIDADES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]

    CATEGORIAS = [
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('red', 'Red'),
        ('accesos', 'Accesos'),
        ('otro', 'Otro'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    estado = models.CharField(max_length=50, choices=ESTADOS, default='abierto')
    prioridad = models.CharField(max_length=50, choices=PRIORIDADES, default='media')
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='otro')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets_creados'
    )

    def crear(self) -> None:
        """Guarda el ticket en el sistema."""
        self.save()

    def modificar(self, **kwargs) -> None:
        """Modifica los atributos del ticket."""
        for campo, valor in kwargs.items():
            setattr(self, campo, valor)
        self.save()

    def eliminar(self) -> None:
        """Elimina el ticket del sistema."""
        self.delete()

    def cambiar_estado(self, nuevo_estado: str) -> None:
        """Cambia el estado del ticket."""
        estados_validos = [e[0] for e in self.ESTADOS]
        if nuevo_estado not in estados_validos:
            raise ValueError(f'Estado no válido: {nuevo_estado}')
        self.estado = nuevo_estado
        self.save()

    def cambiar_prioridad(self, nueva_prioridad: str) -> None:
        """Cambia la prioridad del ticket."""
        prioridades_validas = [p[0] for p in self.PRIORIDADES]
        if nueva_prioridad not in prioridades_validas:
            raise ValueError(f'Prioridad no válida: {nueva_prioridad}')
        self.prioridad = nueva_prioridad
        self.save()

    def __str__(self) -> str:
        return f'[{self.id}] {self.titulo} - {self.estado}'

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['-fecha_creacion']


class Asignacion(models.Model):
    """
    Clase intermedia que modela la relación entre Ticket y Usuario en el contexto de
    la asignación.
    """

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='asignaciones'
    )
    administrador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='asignaciones'
    )
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    def validar(self) -> bool:
        """Comprueba que la asignación es válida."""
        return self.ticket is not None and self.administrador is not None

    def desasignar(self) -> None:
        """Elimina la asignación."""
        self.delete()

    def __str__(self) -> str:
        return f'Ticket {self.ticket.id} → {self.administrador}'

    class Meta:
        verbose_name = 'Asignación'
        verbose_name_plural = 'Asignaciones'
        unique_together = ['ticket', 'administrador']


class VerificarResolucion(models.Model):
    """
    Registra la decisión del usuario final sobre la resolución propuesta por el técnico.
    """

    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        related_name='verificacion_resolucion'
    )
    aceptada = models.BooleanField(default=False)
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def validar(self, aceptada: bool, comentario: str = '') -> None:
        """Registra la decisión del usuario sobre la resolución."""
        self.aceptada = aceptada
        self.comentario = comentario
        self.save()

    def __str__(self) -> str:
        resultado = 'Aceptada' if self.aceptada else 'Rechazada'
        return f'Ticket {self.ticket.id} - {resultado}'

    class Meta:
        verbose_name = 'Verificación de resolución'
        verbose_name_plural = 'Verificaciones de resolución'