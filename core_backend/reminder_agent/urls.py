# reminder_agent/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.medicine_list_create, name='medicine-list-create'),
    path('<int:pk>/', views.medicine_detail, name='medicine-detail'),
    path('trigger/', views.trigger_reminders, name='trigger-reminders'),
]
