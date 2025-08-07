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
    # This path handles the root URL
    path('', home_view, name='home'),
    
    # This path handles the admin site
    path('admin/', admin.site.urls),
    
    # This single path now handles all auth routes (signup, login, etc.)
    path('api/auth/', include('users.urls')),
    
    # These are the paths for your other apps
    path('api/reminder/', include('reminder_agent.urls')),
    path('api/diet/', include('diet_agent.urls')),
]
