from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.template.loader import render_to_string

from .models import ClientRequest
from .forms import ClientRequestForm


def send_client_email(request_obj):
    subject = "We Code We Sketch - Request Received"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [request_obj.email]

    text_content = (
        f"Hi {request_obj.full_name},\n\n"
        f"Thank you for reaching out to We Code We Sketch.\n"
        f"Your request has been received successfully.\n\n"
        f"A copy of your submitted details is included below for your records.\n\n"
        f"Full Name: {request_obj.full_name}\n"
        f"Email: {request_obj.email}\n"
        f"WhatsApp Number: {request_obj.phone}\n"
        f"Service Needed: {request_obj.get_service_display()}\n"
        f"Selected Package: {request_obj.get_package_display() if request_obj.package else 'Not selected'}\n"
        f"Deadline: {request_obj.deadline if request_obj.deadline else 'Not provided'}\n"
        f"Message: {request_obj.message}\n\n"
        f"I will review your request carefully and get back to you as soon as possible.\n\n"
        f"Kind regards,\n"
        f"Forest\n"
        f"We Code We Sketch"
    )

    html_content = render_to_string(
        "emails/client_confirmation.html",
        {
            "name": request_obj.full_name,
            "request_obj": request_obj,
        }
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=to_email,
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


def home(request):
    selected_service = request.GET.get("service")
    selected_package = request.GET.get("package")

    if request.method == "POST":
        form = ClientRequestForm(request.POST)
        if form.is_valid():
            client_request = form.save()

            # Email to business owner
            send_mail(
                subject=f"New Client Request from {client_request.full_name}",
                message=(
                    f"A new enquiry has been submitted.\n\n"
                    f"Full Name: {client_request.full_name}\n"
                    f"Email: {client_request.email}\n"
                    f"WhatsApp Number: {client_request.phone}\n"
                    f"Service Needed: {client_request.get_service_display()}\n"
                    f"Selected Package: "
                    f"{client_request.get_package_display() if client_request.package else 'Not selected'}\n"
                    f"Deadline: {client_request.deadline}\n"
                    f"Message:\n{client_request.message}\n"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            # Branded confirmation email to client
            send_client_email(client_request)

            return redirect("thank_you")
    else:
        form = ClientRequestForm(
            initial={
                "service": selected_service,
                "package": selected_package,
            }
        )

    return render(request, "core/index.html", {"form": form})


def dashboard(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        raise PermissionDenied

    requests = ClientRequest.objects.all()

    total_requests = requests.count()
    new_requests = requests.filter(status="new").count()
    in_progress_requests = requests.filter(status="in_progress").count()
    completed_requests = requests.filter(status="completed").count()

    context = {
        "requests": requests,
        "total_requests": total_requests,
        "new_requests": new_requests,
        "in_progress_requests": in_progress_requests,
        "completed_requests": completed_requests,
    }

    return render(request, "core/dashboard.html", context)


def request_detail(request, request_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        raise PermissionDenied

    client_request = get_object_or_404(ClientRequest, id=request_id)

    if request.method == "POST":
        new_status = request.POST.get("status")

        if new_status in ["new", "in_progress", "completed"]:
            client_request.status = new_status
            client_request.save()

        return redirect("request_detail", request_id=request_id)

    context = {
        "client_request": client_request,
    }

    return render(request, "core/request_detail.html", context)


def delete_request(request, request_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        raise PermissionDenied

    client_request = get_object_or_404(ClientRequest, id=request_id)

    if request.method == "POST":
        client_request.delete()
        return redirect("dashboard")

    return render(
        request,
        "core/delete_request.html",
        {"client_request": client_request},
    )


def thank_you(request):
    return render(request, "core/thank_you.html")


def services(request):
    return render(request, "core/services.html")