# diet_agent/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_profile_view, name='user-profile'),
    path('plan/', views.diet_plan_view, name='diet-plan'),
    path('plan/generate/', views.generate_diet_plan, name='generate-diet-plan'),
]
