from django.urls import path
from portal import views

app_name = 'portal'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('mis-tickets/', views.mis_tickets, name='mis_tickets'),
    path('crear-ticket/', views.crear_ticket, name='crear_ticket'),
]