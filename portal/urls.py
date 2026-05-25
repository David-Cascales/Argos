from django.urls import path
from portal import views

app_name = 'portal'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('mis-tickets/', views.mis_tickets, name='mis_tickets'),
    path('crear-ticket/', views.crear_ticket, name='crear_ticket'),
    path('notificaciones/', views.mis_notificaciones, name='mis_notificaciones'),
    path('notificaciones/marcar-leida/<int:pk>/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
    path('notificaciones/marcar-todas-leidas/', views.marcar_todas_leidas, name='marcar_todas_leidas'),
]