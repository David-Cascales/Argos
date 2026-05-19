from django.urls import path
from panelcontrol import views

app_name = 'panelcontrol'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('tickets/', views.lista_tickets, name='lista_tickets'),
    path('tickets/<int:pk>/', views.detalle_ticket, name='detalle_ticket'),
    
    # 19/05:
    path('tickets/<int:pk>/cambiar-estado/', views.cambiar_estado_ticket, name='cambiar_estado_ticket'),
    path('tickets/<int:pk>/cambiar-prioridad/', views.cambiar_prioridad_ticket, name='cambiar_prioridad_ticket'),
    path('tickets/<int:pk>/asignar/', views.asignar_ticket, name='asignar_ticket'),
    path('tickets/<int:pk>/cerrar/', views.cerrar_ticket, name='cerrar_ticket'),

    path('tickets/exportar/', views.exportar_tickets, name='exportar_tickets'),
    path('inventario/', views.lista_inventario, name='lista_inventario'),
    path('tickets/exportar-pdf/', views.exportar_tickets_pdf, name='exportar_tickets_pdf'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
]