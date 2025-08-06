# diet_agent/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import UserProfile, DietPlan


# --- Agent Integration ---
# Import the actual agent function from the submodule at the project root.
# This requires the project's root directory to be in Python's path.
try:
    from agents.diet_agent_logic.plan_generator import generate_diet_plan as get_structured_diet_plan
except ImportError as e:
    # This fallback prevents the server from crashing if the submodule is not found.
    print(f"CRITICAL IMPORT ERROR: {e}")
    def get_structured_diet_plan(user_input: str):
        print("The 'diet_agent_logic' submodule could not be imported.")
        print("Please ensure it is cloned correctly and that the project root is in sys.path.")
        return None

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
    if request.method == 'POST':
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User profile not found. Please create it first.'}, status=400)

        # Creating a descriptive string from the user's profile to send to the agent
        user_input_string = (
            f"Generate a diet plan for a {profile.age}-year-old with the following details: "
            f"Weight: {profile.weight_kg} kg, Height: {profile.height_cm} cm, "
            f"Activity Level: {profile.activity_level}, Dietary Preference: {profile.dietary_preferences}. "
            f"Allergies: {profile.allergies or 'None'}. "
            f"Health Goals/Issues: {profile.health_issues or 'General Health'}."
        )
        
        # Calling the actual agent function from the submodule
        plan_object = get_structured_diet_plan(user_input_string)

        if not plan_object:
            return JsonResponse({'error': 'Failed to generate diet plan from the agent.'}, status=500)

        # Convert the returned Pydantic object to a dictionary for saving
        generated_plan_dict = plan_object.dict()

        # Deactivate old plans
        DietPlan.objects.filter(user=request.user).update(is_active=False)
        
        # Creating new plan with the agent's response
        new_plan = DietPlan.objects.create(
            user=request.user,
            plan_details=generated_plan_dict,
            is_active=True
        )

        return JsonResponse({'message': 'New diet plan generated.', 'plan': new_plan.plan_details}, status=201)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
