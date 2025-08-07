# diet_agent/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # This path handles GET and POST requests to .../api/diet/profile/
    path('profile/', views.user_profile_view, name='user-profile'),
    
    # This path handles getting the active diet plan
    path('plan/', views.diet_plan_view, name='diet-plan'),
    
    # This path handles generating a new diet plan
    path('plan/generate/', views.generate_diet_plan, name='generate-diet-plan'),
]