from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from tickets.repositories import TicketRepository, AsignacionRepository
from tickets.exports import ExportadorTicketsExcel
from tickets.pdf import ExportadorTicketsPDF
from inventario.repositories import ItemInventarioRepository
from notificaciones.repositories import NotificacionRepository
from cuentas.models import Usuario
from tickets.models import Ticket


@login_required
def inicio(request):
    """Panel de control principal para administradores."""
    total_tickets = len(TicketRepository.obtener_todos())
    tickets_abiertos = len(TicketRepository.obtener_por_estado('abierto'))
    tickets_en_progreso = len(TicketRepository.obtener_por_estado('en_progreso'))
    tickets_resueltos = len(TicketRepository.obtener_por_estado('resuelto'))

    return render(request, 'panelcontrol/inicio.html', {
        'total_tickets': total_tickets,
        'tickets_abiertos': tickets_abiertos,
        'tickets_en_progreso': tickets_en_progreso,
        'tickets_resueltos': tickets_resueltos,
    })


@login_required
def lista_tickets(request):
    """Lista completa de tickets con filtros."""
    estado = request.GET.get('estado', '')
    prioridad = request.GET.get('prioridad', '')
    categoria = request.GET.get('categoria', '')
    tickets = TicketRepository.filtrar(
        estado=estado,
        prioridad=prioridad,
        categoria=categoria
    )
    return render(request, 'panelcontrol/lista_tickets.html', {'tickets': tickets})


@login_required
def detalle_ticket(request, pk):
    """Detalle de un ticket específico."""
    ticket = get_object_or_404(Ticket, pk=pk)
    asignaciones = AsignacionRepository.obtener_por_ticket(ticket)
    administradores = Usuario.objects.filter(is_staff=True)
    return render(request, 'panelcontrol/detalle_ticket.html', {
        'ticket': ticket,
        'asignaciones': asignaciones,
        'administradores': administradores,
        'estados': Ticket.ESTADOS,
        'prioridades': Ticket.PRIORIDADES,
    })


@login_required
def cambiar_estado_ticket(request, pk):
    """Cambia el estado de un ticket."""
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        try:
            ticket.cambiar_estado(nuevo_estado)
            if nuevo_estado == 'cerrado':
                ticket.fecha_cierre = timezone.now()
                ticket.save()
            NotificacionRepository.crear(
                usuario=ticket.creado_por,
                mensaje=f'El estado de tu ticket "{ticket.titulo}" ha cambiado a {ticket.get_estado_display()}.',
                tipo='ticket_actualizado'
            )
            messages.success(request, 'Estado actualizado correctamente.')
        except ValueError as e:
            messages.error(request, str(e))
    return redirect('panelcontrol:detalle_ticket', pk=pk)


@login_required
def cambiar_prioridad_ticket(request, pk):
    """Cambia la prioridad de un ticket."""
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        nueva_prioridad = request.POST.get('prioridad')
        try:
            ticket.cambiar_prioridad(nueva_prioridad)
            messages.success(request, 'Prioridad actualizada correctamente.')
        except ValueError as e:
            messages.error(request, str(e))
    return redirect('panelcontrol:detalle_ticket', pk=pk)


@login_required
def asignar_ticket(request, pk):
    """Asigna un ticket a un administrador."""
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        admin_id = request.POST.get('administrador')
        try:
            administrador = Usuario.objects.get(pk=admin_id)
            AsignacionRepository.crear(ticket=ticket, administrador=administrador)
            NotificacionRepository.crear(
                usuario=administrador,
                mensaje=f'Se te ha asignado el ticket "{ticket.titulo}".',
                tipo='ticket_asignado'
            )
            NotificacionRepository.crear(
                usuario=ticket.creado_por,
                mensaje=f'Tu ticket "{ticket.titulo}" ha sido asignado a {administrador.nombre}.',
                tipo='ticket_actualizado'
            )
            messages.success(request, f'Ticket asignado a {administrador.nombre} correctamente.')
        except Usuario.DoesNotExist:
            messages.error(request, 'El administrador seleccionado no existe.')
        except Exception as e:
            messages.error(request, f'Error al asignar el ticket: {str(e)}')
    return redirect('panelcontrol:detalle_ticket', pk=pk)


@login_required
def cerrar_ticket(request, pk):
    """Cierra un ticket."""
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        ticket.cambiar_estado('cerrado')
        ticket.fecha_cierre = timezone.now()
        ticket.save()
        NotificacionRepository.crear(
            usuario=ticket.creado_por,
            mensaje=f'Tu ticket "{ticket.titulo}" ha sido cerrado.',
            tipo='ticket_resuelto'
        )
        messages.success(request, 'Ticket cerrado correctamente.')
    return redirect('panelcontrol:lista_tickets')


@login_required
def exportar_tickets(request):
    """Exporta los tickets a un archivo Excel."""
    estado = request.GET.get('estado', '')
    prioridad = request.GET.get('prioridad', '')
    categoria = request.GET.get('categoria', '')
    tickets = TicketRepository.filtrar(
        estado=estado,
        prioridad=prioridad,
        categoria=categoria
    )
    return ExportadorTicketsExcel.exportar(tickets)


@login_required
def exportar_tickets_pdf(request):
    """Exporta los tickets a un archivo PDF."""
    estado = request.GET.get('estado', '')
    prioridad = request.GET.get('prioridad', '')
    categoria = request.GET.get('categoria', '')
    tickets = TicketRepository.filtrar(
        estado=estado,
        prioridad=prioridad,
        categoria=categoria
    )
    return ExportadorTicketsPDF.exportar(tickets)


@login_required
def lista_inventario(request):
    """Lista del inventario con filtros."""
    tipo = request.GET.get('tipo', '')
    estado = request.GET.get('estado', '')
    items = ItemInventarioRepository.filtrar(tipo=tipo, estado=estado)
    return render(request, 'panelcontrol/lista_inventario.html', {'items': items})


@login_required
def lista_usuarios(request):
    """Lista de usuarios del sistema."""
    rol = request.GET.get('rol', '')
    activo = request.GET.get('activo', '')
    usuarios = Usuario.objects.all()
    if rol:
        usuarios = usuarios.filter(rol__nombre=rol)
    if activo:
        usuarios = usuarios.filter(is_active=activo == 'true')
    return render(request, 'panelcontrol/lista_usuarios.html', {'usuarios': usuarios})