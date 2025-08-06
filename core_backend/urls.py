# core_backend/urls.py

from django.contrib import admin
from django.urls import path, include
# Ensure the home_view is imported from the correct location
from core_backend.views import home_view 

urlpatterns = [
    # This path handles the root URL
    path('', home_view, name='home'),
    
    # This path handles the admin site
    path('admin/', admin.site.urls),
    
    # This line is crucial. It tells Django to look in 'users.urls'
    # for any URL that starts with 'api/auth/'
    path('api/auth/', include('users.urls')),
    
    # These are the paths for your other apps
    path('api/reminder/', include('reminder_agent.urls')),
    path('api/diet/', include('diet_agent.urls')),
]
