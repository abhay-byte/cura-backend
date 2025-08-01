# diet_agent/models.py

from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    weight_kg = models.FloatField()
    height_cm = models.FloatField()
    activity_level = models.CharField(max_length=50, help_text="e.g., Sedentary, Lightly Active")
    dietary_preferences = models.CharField(max_length=200, help_text="e.g., Vegan, Non-Veg")
    allergies = models.TextField(blank=True, help_text="Comma-separated list of allergies")
    health_issues = models.TextField(blank=True, help_text="e.g., Diabetes, High Blood Pressure")

    def __str__(self):
        return f"Profile for {self.user.username}"

class DietPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan_details = models.JSONField() # Store the generated diet plan as JSON
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Diet plan for {self.user.username} on {self.created_at.date()}"
