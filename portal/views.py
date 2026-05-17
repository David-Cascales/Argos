from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tickets.repositories import TicketRepository
from tickets.forms import TicketForm


@login_required
def inicio(request):
    """Página principal del portal de usuarios."""
    tickets = TicketRepository.obtener_por_usuario(request.user)
    return render(request, 'portal/inicio.html', {'tickets': tickets})


@login_required
def mis_tickets(request):
    """Lista de tickets del usuario con filtros."""
    estado = request.GET.get('estado', '')
    tickets = TicketRepository.obtener_por_usuario(request.user)
    if estado:
        tickets = tickets.filter(estado=estado)
    return render(request, 'portal/mis_tickets.html', {'tickets': tickets})


@login_required
def crear_ticket(request):
    """Formulario para crear un nuevo ticket."""
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            TicketRepository.crear(form.cleaned_data, request.user)
            messages.success(request, 'Ticket creado correctamente.')
            return redirect('portal:mis_tickets')
    else:
        form = TicketForm()
    return render(request, 'portal/crear_ticket.html', {'form': form})