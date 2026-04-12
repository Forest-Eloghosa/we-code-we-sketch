from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import ClientRequest
from .forms import ClientRequestForm


def home(request):
    selected_service = request.GET.get("service")
    selected_package = request.GET.get("package")

    if request.method == "POST":
        form = ClientRequestForm(request.POST)
        if form.is_valid():
            client_request = form.save()

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

            send_mail(
                subject="We Code We Sketch - Request Received",
                message=(
                    f"Hi {client_request.full_name},\n\n"
                    f"Thank you for reaching out to We Code We Sketch.\n"
                    f"I’ve received your enquiry and will get back to you as soon as possible.\n\n"
                    f"In the meantime, thank you for your patience.\n\n"
                    f"Best regards,\n"
                    f"Forest\n"
                    f"We Code We Sketch"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client_request.email],
                fail_silently=False,
            )

            return redirect("thank_you")
    else:
        form = ClientRequestForm(initial={
            "service": selected_service,
            "package": selected_package,
        })

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


def send_client_email(request_obj):
    subject = "We Code We Sketch - Request Received"
    from_email = "wecodewesketch@gmail.com"
    to_email = request_obj.email

    html_content = render_to_string(
        "emails/client_confirmation.html",
        {
            "name": request_obj.full_name
        }
    )

    email = EmailMultiAlternatives(subject, "", from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()


def thank_you(request):
    return render(request, "core/thank_you.html")


def services(request):
    return render(request, "core/services.html")