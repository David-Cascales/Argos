from django.db import models
from django.conf import settings


class ItemInventario(models.Model):
    """
    Representa cualquier recurso tecnológico registrado en el inventario de la organización.
    """

    TIPOS = [
        ('ordenador', 'Ordenador'),
        ('impresora', 'Impresora'),
        ('monitor', 'Monitor'),
        ('servidor', 'Servidor'),
        ('switch', 'Switch'),
        ('router', 'Router'),
        ('telefono', 'Teléfono'),
        ('otro', 'Otro'),
    ]

    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('en_reparacion', 'En reparación'),
        ('dado_de_baja', 'Dado de baja'),
    ]

    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=50, choices=TIPOS)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=50, choices=ESTADOS, default='activo')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    gestionado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inventario'
    )

    def crear(self) -> None:
        """Guarda el item en el inventario."""
        self.save()

    def eliminar(self) -> None:
        """Elimina el item del inventario."""
        self.delete()

    def __str__(self) -> str:
        return f'{self.nombre} ({self.tipo})'

    class Meta:
        verbose_name = 'Item de inventario'
        verbose_name_plural = 'Items de inventario'
        ordering = ['nombre']