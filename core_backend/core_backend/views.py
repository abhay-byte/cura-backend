from django.http import JsonResponse

def home_view(request):
    """
    A simple view for the root URL to confirm the API is running.
    """
    return JsonResponse({
        'status': 'ok',
        'message': 'Welcome to the CURA AI Health Agents API!',
        'documentation': 'https://github.com/abhay-byte/cura-backend/blob/main/docs/api.md'
    })
