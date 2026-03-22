from django.shortcuts import render, redirect
from .forms import ClientRequestForm

 
# Create your views here.

def home(request):
    selected_service = request.GET.get("service")

    if request.method == "POST":
        form = ClientRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("thank_you")
    else:
        form = ClientRequestForm(initial={"service": selected_service})

    return render(request, "core/index.html", {"form": form})


def thank_you(request):
    return render(request, "core/thank-you.html")

def services(request):
    return render(request, "core/services.html")