import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser

@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            if not all([username, password, email]):
                return JsonResponse({'error': 'Username, password, and email are required.'}, status=400)

            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already in use.'}, status=400)
            
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists.'}, status=400)

            user = CustomUser.objects.create_user(username=username, password=password, email=email)
            return JsonResponse({'message': 'User created successfully.'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'error': 'Only POST method is allowed.'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({'error': 'Email and password are required.'}, status=400)

            # Authenticate using email
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({
                    'message': f'Welcome back, {user.username}!',
                    'userId': user.id,
                    'email': user.email
                })
            else:
                # Fallback to check username for authentication
                user = authenticate(request, username=data.get('username'), password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({
                        'message': f'Welcome back, {user.username}!',
                        'userId': user.id,
                        'email': user.email
                    })
                return JsonResponse({'error': 'Invalid credentials.'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    return JsonResponse({'error': 'Only POST method is allowed.'}, status=405)
