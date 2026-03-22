from django.contrib import admin
from .models import ClientRequest

# Register your models here.



@admin.register(ClientRequest)
class ClientRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "service", "status", "deadline", "created_at")
    search_fields = ("full_name", "email", "message")
    list_filter = ("service", "status", "created_at")