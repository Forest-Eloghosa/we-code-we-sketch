from django.db import models

# Create your models here.

class ClientRequest(models.Model):
    SERVICE_CHOICES = [
        ("digital-assistance", "Digital Assistance"),
        ("application-support", "Student Application Support"),
        ("admission-payment", "Admission Payment Assistance"),
        ("cv-review", "CV Review"),
        ("portfolio-website", "Portfolio Website"),
    ]

    STATUS_CHOICES = [
        ("new", "New"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    deadline = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.get_service_display()} - {self.get_status_display()}"