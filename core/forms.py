from django import forms
from .models import ClientRequest


class ClientRequestForm(forms.ModelForm):
    class Meta:
        model = ClientRequest
        fields = ["full_name", "email", "phone", "service", "deadline", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Your full name"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-input",
                "placeholder": "Your email address"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Your WhatsApp number"
            }),
            "service": forms.Select(attrs={
                "class": "form-input"
            }),
            "deadline": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Example: 30 March 2026"
            }),
            "message": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "Tell me a little about the support you need...",
                "rows": 6
            }),
        }
        labels = {
            "full_name": "Full Name",
            "email": "Email Address",
            "phone": "WhatsApp Number",
            "service": "Service Needed",
            "deadline": "Deadline (if any)",
            "message": "How can I help?",
        }