from notificaciones.models import Notificacion


class NotificacionRepository:
    """
    Repositorio para el modelo Notificacion.
    Se aplica el patrón Repository: se centraliza el acceso a datos de Notificacion.
    """

    @staticmethod
    def obtener_por_usuario(usuario) -> list:
        return Notificacion.objects.filter(usuario=usuario)

    @staticmethod
    def obtener_no_leidas(usuario) -> list:
        return Notificacion.objects.filter(usuario=usuario, leido=False)

    @staticmethod
    def crear(usuario, mensaje: str, tipo: str) -> Notificacion:
        notificacion = Notificacion(
            usuario=usuario,
            mensaje=mensaje,
            tipo=tipo
        )
        notificacion.save()
        return notificacion

    @staticmethod
    def marcar_todas_leidas(usuario) -> None:
        Notificacion.objects.filter(usuario=usuario, leido=False).update(leido=True)