from django.urls import path
from panelcontrol import views

app_name = 'panelcontrol'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('tickets/', views.lista_tickets, name='lista_tickets'),
    path('tickets/<int:pk>/', views.detalle_ticket, name='detalle_ticket'),
    
    # 19/05 - logica de negocio de los tickets:
    path('tickets/<int:pk>/cambiar-estado/', views.cambiar_estado_ticket, name='cambiar_estado_ticket'),
    path('tickets/<int:pk>/cambiar-prioridad/', views.cambiar_prioridad_ticket, name='cambiar_prioridad_ticket'),
    path('tickets/<int:pk>/asignar/', views.asignar_ticket, name='asignar_ticket'),
    path('tickets/<int:pk>/cerrar/', views.cerrar_ticket, name='cerrar_ticket'),

    # 19/05 - gestion de usuarios:
    path('usuarios/<int:pk>/', views.detalle_usuario, name='detalle_usuario'),
    path('usuarios/<int:pk>/cambiar-rol/', views.cambiar_rol_usuario, name='cambiar_rol_usuario'),
    path('usuarios/<int:pk>/toggle-activo/', views.toggle_activo_usuario, name='toggle_activo_usuario'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),

    path('tickets/exportar/', views.exportar_tickets, name='exportar_tickets'),
    path('inventario/', views.lista_inventario, name='lista_inventario'),
    path('tickets/exportar-pdf/', views.exportar_tickets_pdf, name='exportar_tickets_pdf'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
]