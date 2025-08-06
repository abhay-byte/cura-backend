# health_agents/urls.py

from django.contrib import admin
from django.urls import path, include
from users.views import signup_view, login_view
from core_backend.views import home_view 


# Reminder Agent URLs
reminder_urls = [
    path('medicines/', include('reminder_agent.urls')),
    # You would add more paths here, e.g., for reminders
]

# Diet Agent URLs
diet_urls = [
    path('profile/', include('diet_agent.urls')),
    # You would add more paths here, e.g., for diet plans
]

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    
    # Auth endpoints
    path('api/signup/', signup_view, name='signup'),
    path('api/login/', login_view, name='login'),
    
    # App-specific endpoints
    path('api/reminder/', include(reminder_urls)),
    path('api/diet/', include(diet_urls)),
]
