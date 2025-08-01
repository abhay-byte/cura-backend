# diet_agent/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import UserProfile, DietPlan

# --- User Profile Endpoint ---

@csrf_exempt
@login_required
def user_profile_view(request):
    # Get or create/update the profile for the logged-in user
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        return JsonResponse({
            'age': profile.age,
            'weight_kg': profile.weight_kg,
            'height_cm': profile.height_cm,
            'dietary_preferences': profile.dietary_preferences,
            'allergies': profile.allergies,
            'health_issues': profile.health_issues
        })
    elif request.method in ['POST', 'PUT']:
        try:
            data = json.loads(request.body)
            # Update profile fields from data...
            profile.age = data.get('age', profile.age)
            profile.weight_kg = data.get('weight_kg', profile.weight_kg)
            # ... and so on for other fields
            profile.save()
            return JsonResponse({'message': 'Profile updated.'})
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data.'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


# --- Diet Plan Endpoints ---

@csrf_exempt
@login_required
def diet_plan_view(request):
    # Get the current active diet plan
    if request.method == 'GET':
        try:
            plan = DietPlan.objects.get(user=request.user, is_active=True)
            return JsonResponse(plan.plan_details, safe=False)
        except DietPlan.DoesNotExist:
            return JsonResponse({'error': 'No active diet plan found. Generate one first.'}, status=404)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@login_required
def generate_diet_plan(request):
    """
    This is where the core AGENT logic for PS2 will go.
    """
    if request.method == 'POST':
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User profile not found. Please create it first.'}, status=400)

        # 1. Get user profile data (age, weight, goals, allergies, etc.).
        # 2. Pass this data to the Diet Agent (your AI/business logic).
        # 3. The agent returns a structured diet plan (JSON).
        # 4. Save the new plan and deactivate old ones.
        
        print(f"AGENT LOGIC: Generating diet plan for {request.user.email}...")
        
        # --- PLACEHOLDER for Agent Response ---
        mock_diet_plan = {
            "daily_calories": 2000,
            "meals": {
                "breakfast": {"name": "Oatmeal with Berries", "time": "08:00"},
                "lunch": {"name": "Grilled Chicken Salad", "time": "13:00"},
                "dinner": {"name": "Salmon with Quinoa", "time": "19:00"}
            },
            "grocery_list": ["Oats", "Berries", "Chicken Breast", "Lettuce", "Salmon", "Quinoa"],
            "notes": "Drink 8 glasses of water."
        }
        # --- End Placeholder ---

        # Deactivate old plans
        DietPlan.objects.filter(user=request.user).update(is_active=False)
        
        # Create new plan
        new_plan = DietPlan.objects.create(
            user=request.user,
            plan_details=mock_diet_plan
        )

        return JsonResponse({'message': 'New diet plan generated.', 'plan': new_plan.plan_details}, status=201)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
