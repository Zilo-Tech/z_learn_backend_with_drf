from django.urls import path
from . import views

urlpatterns = [
    path('export-users/', views.export_users_to_csv, name='export_users_to_csv'),
    path('send-whatsapp-message/', views.send_whatsapp_message, name='send_whatsapp_message'),
]