from django.urls import path
from panelcontrol import views

app_name = 'panelcontrol'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('tickets/', views.lista_tickets, name='lista_tickets'),
    path('tickets/<int:pk>/', views.detalle_ticket, name='detalle_ticket'),
    path('tickets/exportar/', views.exportar_tickets, name='exportar_tickets'),
    path('inventario/', views.lista_inventario, name='lista_inventario'),
    path('tickets/exportar-pdf/', views.exportar_tickets_pdf, name='exportar_tickets_pdf'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
]