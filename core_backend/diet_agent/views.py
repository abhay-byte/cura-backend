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
    # Get or create the profile for the logged-in user
    # .get_or_create returns a tuple (object, created_boolean)
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        # For a new profile, these might be null or default values
        return JsonResponse({
            'age': profile.age,
            'weight_kg': profile.weight_kg,
            'height_cm': profile.height_cm,
            'activity_level': profile.activity_level,
            'dietary_preferences': profile.dietary_preferences,
            'allergies': profile.allergies,
            'health_issues': profile.health_issues
        })
        
    elif request.method in ['POST', 'PUT']:
        try:
            data = json.loads(request.body)
            # Update profile fields from data, keeping existing values if a field is not provided
            profile.age = data.get('age', profile.age)
            profile.weight_kg = data.get('weight_kg', profile.weight_kg)
            profile.height_cm = data.get('height_cm', profile.height_cm)
            profile.activity_level = data.get('activity_level', profile.activity_level)
            profile.dietary_preferences = data.get('dietary_preferences', profile.dietary_preferences)
            profile.allergies = data.get('allergies', profile.allergies)
            profile.health_issues = data.get('health_issues', profile.health_issues)
            
            profile.save()
            return JsonResponse({'message': 'Profile updated successfully.'})
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

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
        # This is a complete, structured example of what the agent should return.
        mock_diet_plan = {
          "daily_calories": 2150,
          "macronutrients": {
            "protein_grams": 150,
            "carbs_grams": 200,
            "fat_grams": 80
          },
          "meals": {
            "breakfast": {
              "name": "Greek Yogurt with Almonds and Berries",
              "time": "08:00",
              "calories": 400,
              "notes": "A great source of protein to start your day."
            },
            "lunch": {
              "name": "Quinoa Salad with Chickpeas and Avocado",
              "time": "13:00",
              "calories": 650,
              "notes": "Rich in fiber and healthy fats."
            },
            "snack": {
              "name": "Apple with Peanut Butter",
              "time": "16:00",
              "calories": 250,
              "notes": ""
            },
            "dinner": {
              "name": "Baked Salmon with Asparagus and Sweet Potato",
              "time": "19:30",
              "calories": 850,
              "notes": "Excellent source of Omega-3 fatty acids."
            }
          },
          "grocery_list": [
            "Greek Yogurt", "Almonds", "Mixed Berries", "Quinoa",
            "Chickpeas", "Avocado", "Apple", "Peanut Butter",
            "Salmon Fillet", "Asparagus", "Sweet Potato"
          ],
          "notes": "Remember to drink at least 8 glasses of water throughout the day."
        }
        # --- End Placeholder ---

        # Deactivate any previous plans for this user
        DietPlan.objects.filter(user=request.user).update(is_active=False)
        
        # Create the new active plan
        new_plan = DietPlan.objects.create(
            user=request.user,
            plan_details=mock_diet_plan,
            is_active=True
        )

        return JsonResponse({'message': 'New diet plan generated.', 'plan': new_plan.plan_details}, status=201)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
