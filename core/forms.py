from django import forms
from .models import ClientRequest


class ClientRequestForm(forms.ModelForm):
    class Meta:
        model = ClientRequest
        fields = [
            "full_name",
            "email",
            "phone",
            "service",
            "package",
            "deadline",
            "message",
        ]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "First and last name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Your email address",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Your WhatsApp number",
                }
            ),
            "service": forms.Select(
                attrs={
                    "class": "form-input",
                }
            ),
            "package": forms.Select(
                attrs={
                    "class": "form-input",
                }
            ),
            "deadline": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Example: 30 March 2026",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "placeholder": "Tell me a little about the support you need...",
                    "rows": 6,
                }
            ),
        }
        labels = {
            "full_name": "Full Name",
            "email": "Email Address",
            "phone": "WhatsApp Number",
            "service": "Service Needed",
            "package": "Selected Package",
            "deadline": "Deadline (if any)",
            "message": "How can I help?",
        }

    def clean_full_name(self):
        full_name = self.cleaned_data["full_name"].strip()
        parts = [part for part in full_name.split() if part]

        if len(parts) < 2:
            raise forms.ValidationError(
                "Please enter your full name (first and last name)."
            )

        return full_name