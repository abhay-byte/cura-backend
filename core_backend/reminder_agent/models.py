# reminder_agent/models.py

from django.db import models
from django.conf import settings

class Medicine(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50, help_text="e.g., 500mg")
    inventory = models.PositiveIntegerField(default=0, help_text="e.g., number of pills")
    refill_threshold = models.PositiveIntegerField(default=10, help_text="Notify when inventory falls below this")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.dosage}) for {self.user.username}"

class Reminder(models.Model):
    INSTRUCTION_CHOICES = [
        ('Before Food', 'Before Food'),
        ('After Food', 'After Food'),
        ('With Food', 'With Food'),
        ('Any Time', 'Any Time'),
    ]

    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='reminders')
    reminder_time = models.TimeField()
    quantity = models.PositiveIntegerField(default=1)
    instruction = models.CharField(max_length=20, choices=INSTRUCTION_CHOICES, default='Any Time')
    is_active = models.BooleanField(default=True)
    last_notified = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Reminder for {self.medicine.name} at {self.reminder_time}"
