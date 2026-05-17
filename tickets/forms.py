from django import forms
from tickets.models import Ticket


class TicketForm(forms.ModelForm):
    """
    Formulario para la creación y edición de tickets.
    Se aplica el patrón Factory: centraliza la creación de formularios de Ticket.
    """

    class Meta:
        model = Ticket
        fields = ['titulo', 'descripcion', 'categoria', 'prioridad']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'campo-formulario',
                'placeholder': 'Título de la incidencia'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'campo-formulario',
                'placeholder': 'Describe la incidencia con detalle',
                'rows': 5
            }),
            'categoria': forms.Select(attrs={
                'class': 'campo-formulario'
            }),
            'prioridad': forms.Select(attrs={
                'class': 'campo-formulario'
            }),
        }
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'categoria': 'Categoría',
            'prioridad': 'Prioridad',
        }


class FiltroTicketForm(forms.Form):
    """
    Formulario para filtrar tickets en el panel de control.
    """

    estado = forms.ChoiceField(
        choices=[('', 'Todos los estados')] + Ticket.ESTADOS,
        required=False,
        widget=forms.Select(attrs={'class': 'campo-formulario'})
    )
    prioridad = forms.ChoiceField(
        choices=[('', 'Todas las prioridades')] + Ticket.PRIORIDADES,
        required=False,
        widget=forms.Select(attrs={'class': 'campo-formulario'})
    )
    categoria = forms.ChoiceField(
        choices=[('', 'Todas las categorías')] + Ticket.CATEGORIAS,
        required=False,
        widget=forms.Select(attrs={'class': 'campo-formulario'})
    )