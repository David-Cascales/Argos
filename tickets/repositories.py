from tickets.models import Ticket, Asignacion, VerificarResolucion


class TicketRepository:
    """
    Repositorio para el modelo Ticket.
    Se aplica el patrón Repository: se centraliza el acceso a datos de Ticket, desacoplando
    la lógica de negocio de la capa de persistencia.
    """

    @staticmethod
    def obtener_todos() -> list:
        return Ticket.objects.all()

    @staticmethod
    def obtener_por_id(ticket_id: int) -> Ticket:
        return Ticket.objects.get(id=ticket_id)

    @staticmethod
    def obtener_por_usuario(usuario) -> list:
        return Ticket.objects.filter(creado_por=usuario)

    @staticmethod
    def obtener_por_estado(estado: str) -> list:
        return Ticket.objects.filter(estado=estado)

    @staticmethod
    def obtener_por_prioridad(prioridad: str) -> list:
        return Ticket.objects.filter(prioridad=prioridad)

    @staticmethod
    def obtener_por_categoria(categoria: str) -> list:
        return Ticket.objects.filter(categoria=categoria)

    @staticmethod
    def filtrar(estado: str = None, prioridad: str = None, categoria: str = None) -> list:
        queryset = Ticket.objects.all()
        if estado:
            queryset = queryset.filter(estado=estado)
        if prioridad:
            queryset = queryset.filter(prioridad=prioridad)
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        return queryset

    @staticmethod
    def crear(datos: dict, usuario) -> Ticket:
        ticket = Ticket(creado_por=usuario, **datos)
        ticket.save()
        return ticket

    @staticmethod
    def actualizar(ticket: Ticket, datos: dict) -> Ticket:
        for campo, valor in datos.items():
            setattr(ticket, campo, valor)
        ticket.save()
        return ticket

    @staticmethod
    def eliminar(ticket: Ticket) -> None:
        ticket.delete()


class AsignacionRepository:
    """
    Repositorio para el modelo Asignacion.
    Se centraliza el acceso a datos de Asignacion.
    """

    @staticmethod
    def obtener_por_ticket(ticket: Ticket) -> list:
        return Asignacion.objects.filter(ticket=ticket)

    @staticmethod
    def obtener_por_administrador(administrador) -> list:
        return Asignacion.objects.filter(administrador=administrador)

    @staticmethod
    def crear(ticket: Ticket, administrador) -> Asignacion:
        asignacion = Asignacion(ticket=ticket, administrador=administrador)
        asignacion.save()
        return asignacion

    @staticmethod
    def eliminar(asignacion: Asignacion) -> None:
        asignacion.delete()


class VerificarResolucionRepository:
    """
    Repositorio para el modelo VerificarResolucion.
    Se centraliza el acceso a datos de VerificarResolucion.
    """

    @staticmethod
    def obtener_por_ticket(ticket: Ticket) -> VerificarResolucion:
        return VerificarResolucion.objects.get(ticket=ticket)

    @staticmethod
    def crear(ticket: Ticket, aceptada: bool, comentario: str = '') -> VerificarResolucion:
        verificacion = VerificarResolucion(
            ticket=ticket,
            aceptada=aceptada,
            comentario=comentario
        )
        verificacion.save()
        return verificacion