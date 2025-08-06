# core_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from core_backend.views import home_view 

urlpatterns = [
    path('', home_view, name='home'), 
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/reminder/', include('reminder_agent.urls')),
    path('api/diet/', include('diet_agent.urls')),
]