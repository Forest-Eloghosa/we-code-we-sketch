from .models import ClientRequest

def new_requests_count(request):
    if request.user.is_authenticated and request.user.is_superuser:
        count = ClientRequest.objects.filter(status="new").count()
        return {"new_requests_count": count}
    return {}