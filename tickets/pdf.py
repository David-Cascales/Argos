from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from django.http import HttpResponse
from tickets.repositories import TicketRepository


class ExportadorTicketsPDF:
    """
    Clase responsable de exportar tickets a PDF.
    Patrón Strategy: define una estrategia concreta de exportación.
    """

    COLOR_PRIMARIO = colors.HexColor('#2563EB')
    COLOR_CABECERA_TEXTO = colors.white
    COLOR_FILA_PAR = colors.HexColor('#F1F5F9')

    @staticmethod
    def exportar(queryset=None) -> HttpResponse:
        """
        Genera un archivo PDF con los tickets proporcionados
        y lo devuelve como respuesta HTTP descargable.
        """
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="tickets.pdf"'

        doc = SimpleDocTemplate(
            response,
            pagesize=A4,
            rightMargin=1.5 * cm,
            leftMargin=1.5 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm
        )

        estilos = getSampleStyleSheet()
        estilo_titulo = ParagraphStyle(
            'Titulo',
            parent=estilos['Heading1'],
            textColor=ExportadorTicketsPDF.COLOR_PRIMARIO,
            fontSize=18,
            spaceAfter=0.5 * cm
        )
        estilo_subtitulo = ParagraphStyle(
            'Subtitulo',
            parent=estilos['Normal'],
            textColor=colors.HexColor('#64748B'),
            fontSize=10,
            spaceAfter=1 * cm
        )

        elementos = []

        # Título
        elementos.append(Paragraph('Argos - Gestor de Incidencias', estilo_titulo))
        elementos.append(Paragraph('Informe de tickets', estilo_subtitulo))
        elementos.append(Spacer(1, 0.5 * cm))

        # Datos de la tabla
        cabeceras = ['ID', 'Título', 'Estado', 'Prioridad', 'Categoría', 'Creado por', 'Fecha']
        datos = [cabeceras]

        tickets = queryset if queryset is not None else TicketRepository.obtener_todos()
        for ticket in tickets:
            datos.append([
                str(ticket.id),
                ticket.titulo[:40] + '...' if len(ticket.titulo) > 40 else ticket.titulo,
                ticket.get_estado_display(),
                ticket.get_prioridad_display(),
                ticket.get_categoria_display(),
                ticket.creado_por.nombre,
                ticket.fecha_creacion.strftime('%d/%m/%Y'),
            ])

        # Estilo de la tabla
        tabla = Table(datos, repeatRows=1)
        tabla.setStyle(TableStyle([
            # Cabecera
            ('BACKGROUND', (0, 0), (-1, 0), ExportadorTicketsPDF.COLOR_PRIMARIO),
            ('TEXTCOLOR', (0, 0), (-1, 0), ExportadorTicketsPDF.COLOR_CABECERA_TEXTO),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),

            # Filas de datos
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),

            # Filas alternas
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
                colors.white,
                ExportadorTicketsPDF.COLOR_FILA_PAR
            ]),

            # Bordes
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('BOX', (0, 0), (-1, -1), 1, ExportadorTicketsPDF.COLOR_PRIMARIO),
        ]))

        elementos.append(tabla)
        doc.build(elementos)
        return response