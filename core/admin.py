from django.contrib import admin
from .models import ClientRequest


@admin.register(ClientRequest)
class ClientRequestAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "service",
        "package",
        "status",
        "deadline",
        "created_at",
    )
    list_filter = ("service", "package", "status", "created_at")
    search_fields = ("full_name", "email", "phone", "message")
    list_editable = ("status",)
    ordering = ("-created_at",)   