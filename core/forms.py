from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import ClientRequest
import re


class ClientRequestForm(forms.ModelForm):
    # Hidden anti-spam field. Real users will not see it.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
     super().__init__(*args, **kwargs)

     service = self.data.get("service") or self.initial.get("service")

     if service == "cv-review":
        self.fields["package"].choices = [
            ("", "---------"),
            ("cv-review", "CV Review"),
        ]

     elif service == "cv-creation":
        self.fields["package"].choices = [
            ("", "---------"),
            ("cv-creation", "CV Creation"),
        ]

     elif service == "application-support":
        self.fields["package"].choices = [
            ("", "---------"),
            ("standard-application-package", "Standard Application Package"),
            ("priority-application-package", "Priority Application Package"),
        ]

     elif service == "admission-payment":
        self.fields["package"].choices = [
            ("", "---------"),
            ("basic-application-support", "Basic Application Support"),
        ]

     elif service == "digital-assistance":
        self.fields["package"].choices = [
            ("", "---------"),
            ("express-assistance", "Express Assistance"),
            ("general-digital-assistance", "General Digital Assistance"),
        ]

     elif service == "consultation":
        self.fields["package"].choices = [
            ("", "---------"),
            ("consultation", "Consultation"),
        ]

     elif service == "travel-documentation":
        self.fields["package"].choices = [
            ("", "---------"),
            ("travel-documentation-support", "Travel Documentation Support"),
        ]

     elif service == "portfolio-website":
        self.fields["package"].choices = [
            ("", "---------"),
            ("portfolio-website", "Portfolio Website"),
        ]

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get("email")
        phone = cleaned_data.get("phone")

        recent_time = timezone.now() - timedelta(minutes=10)

        if email and ClientRequest.objects.filter(
            email=email,
            created_at__gte=recent_time
        ).exists():
            raise forms.ValidationError(
                "You have already submitted a request recently. Please wait before submitting again."
            )

        if phone and ClientRequest.objects.filter(
            phone=phone,
            created_at__gte=recent_time
        ).exists():
            raise forms.ValidationError(
                "A request with this WhatsApp number was submitted recently. Please wait before submitting again."
            )

        return cleaned_data

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
            "full_name": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "First and last name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-input",
                "placeholder": "Your email address",
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Example: +353899647256",
            }),
            "service": forms.Select(attrs={"class": "form-input"}),
            "package": forms.Select(attrs={"class": "form-input"}),
            "deadline": forms.DateInput(attrs={
                "class": "form-input",
                 "type": "date",
            }),
            "message": forms.Textarea(attrs={
                "class": "form-input",
                "placeholder": "Tell me a little about the support you need...",
                "rows": 6,
            }),
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

    def clean_website(self):
        website = self.cleaned_data.get("website")
        if website:
            raise forms.ValidationError("Spam detected.")
        return website

    def clean_full_name(self):
        full_name = self.cleaned_data["full_name"].strip()
        parts = [part for part in full_name.split() if part]

        blocked_words = ["first", "name", "test", "fake", "admin", "user"]

        if len(parts) < 2:
            raise forms.ValidationError(
                "Please enter your full name, including first and last name."
            )

        if any(word.lower() in blocked_words for word in parts):
            raise forms.ValidationError(
                "Please enter your real full name."
            )

        if any(len(part) < 3 for part in parts):
            raise forms.ValidationError(
                "Each part of your name should be at least 3 letters."
            )

        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$", full_name):
            raise forms.ValidationError(
                "Please enter a valid name using letters only."
            )

        return " ".join(part.capitalize() for part in parts)

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        blocked_keywords = [
            "test",
            "fake",
            "noemail",
            "none",
            "admin",
            "example",
            "demo",
        ]

        local_part = email.split("@")[0]

        if any(keyword in local_part for keyword in blocked_keywords):
            raise forms.ValidationError("Please enter a real email address.")

        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()

        if not phone:
            return phone

        # Allows +, spaces, brackets and dashes, but checks real digit length.
        digits_only = re.sub(r"\D", "", phone)

        if len(digits_only) < 7 or len(digits_only) > 15:
            raise forms.ValidationError("Please enter a valid WhatsApp number.")

        return phone

    def clean_message(self):
        message = self.cleaned_data["message"].strip()

        if len(message) < 20:
            raise forms.ValidationError(
                "Please provide a little more detail about what you need help with."
            )

        spam_phrases = [
    "seo optimization",
    "search engine optimization",
    "rank on google",
    "backend of your website",
    "quick call",
    "website issues",
    "your website is not ranking",
    "improve your website",
    "google ranking",
    "first page of google",
    "increase traffic",
    "digital marketing",
    "web solution",
    "websolution",
]

        if any(phrase in message.lower() for phrase in spam_phrases):
            raise forms.ValidationError(
                "This form is for client support requests only."
            )

        return message