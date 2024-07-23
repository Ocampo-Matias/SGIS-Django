from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class incidents(models.Model):
    INCIDENT_TYPES = [
        ('phishing', 'Phishing'),
        ('malware', 'Malware'),
        ('data_breach', 'Data Breach'),
        ('ddos', 'DDoS Attack'),
    ]

    INCIDENT_STATES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    PRIORITY = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    incident_id = models.AutoField(primary_key=True)
    incident_type = models.CharField(max_length=100, choices=INCIDENT_TYPES)
    date_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    priority = models.CharField(
        max_length=100, choices=PRIORITY, default='low')
    state = models.CharField(
        max_length=100, choices=INCIDENT_STATES, default='new')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    history_incident = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Incident {self.incident_id} - {self.incident_type}"


class comment(models.Model):
    incident = models.ForeignKey(
        incidents, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('upper_level', 'Upper_Level'),
        ('medium_level', 'Medium_Level'),
        ('low_level', 'Low_Level'),
    ]
    role = models.CharField(
        max_length=100, choices=ROLE_CHOICES, default='low_level')

    def __str__(self):
        return self.username

