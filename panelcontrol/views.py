from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tickets.repositories import TicketRepository, AsignacionRepository
from inventario.repositories import ItemInventarioRepository
from cuentas.models import Usuario
from tickets.exports import ExportadorTicketsExcel
from tickets.pdf import ExportadorTicketsPDF

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
    ticket = get_object_or_404(
        TicketRepository.obtener_todos().model, pk=pk
    )
    asignaciones = AsignacionRepository.obtener_por_ticket(ticket)
    return render(request, 'panelcontrol/detalle_ticket.html', {
        'ticket': ticket,
        'asignaciones': asignaciones,
    })


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
        usuarios = usuarios.filter(activo=activo == 'true')
    return render(request, 'panelcontrol/lista_usuarios.html', {'usuarios': usuarios})

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