# reminder_agent/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Medicine URLs
    path('medicines/', views.medicine_list_create, name='medicine-list-create'),
    path('medicines/<int:pk>/', views.medicine_detail, name='medicine-detail'),
    
    # Reminder URLs
    path('medicines/<int:medicine_pk>/reminders/', views.reminder_create, name='reminder-create'),
    path('reminders/<int:reminder_pk>/take/', views.take_medicine, name='take-medicine'),

    # Agent Trigger URL
    path('trigger/', views.trigger_reminders, name='trigger-reminders'),
]
