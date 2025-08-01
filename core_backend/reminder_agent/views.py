# reminder_agent/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Medicine, Reminder

# Helper to check ownership
def is_owner(user, model_instance):
    return user == model_instance.user

# --- Medicine Endpoints ---

@csrf_exempt
@login_required
def medicine_list_create(request):
    # List all medicines for the logged-in user
    if request.method == 'GET':
        medicines = Medicine.objects.filter(user=request.user)
        data = [{
            'id': med.id,
            'name': med.name,
            'dosage': med.dosage,
            'inventory': med.inventory
        } for med in medicines]
        return JsonResponse(data, safe=False)

    # Create a new medicine
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            medicine = Medicine.objects.create(
                user=request.user,
                name=data['name'],
                dosage=data['dosage'],
                inventory=data.get('inventory', 0)
            )
            return JsonResponse({'message': 'Medicine added.', 'id': medicine.id}, status=201)
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data.'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@login_required
def medicine_detail(request, pk):
    try:
        medicine = Medicine.objects.get(pk=pk)
        if not is_owner(request.user, medicine):
            return JsonResponse({'error': 'Not authorized.'}, status=403)
    except Medicine.DoesNotExist:
        return JsonResponse({'error': 'Medicine not found.'}, status=404)

    # Get, Update, or Delete a specific medicine
    if request.method == 'GET':
        return JsonResponse({
            'id': medicine.id,
            'name': medicine.name,
            'dosage': medicine.dosage,
            'inventory': medicine.inventory
        })
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            # Update fields with new data, keeping old data if a field is not provided
            medicine.name = data.get('name', medicine.name)
            medicine.dosage = data.get('dosage', medicine.dosage)
            medicine.inventory = data.get('inventory', medicine.inventory)
            medicine.refill_threshold = data.get('refill_threshold', medicine.refill_threshold)
            medicine.save()
            return JsonResponse({'message': 'Medicine updated successfully.'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
            
    elif request.method == 'DELETE':
        medicine.delete()
        return JsonResponse({'message': 'Medicine deleted.'}, status=204)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# --- Reminder Endpoints ---

@csrf_exempt
@login_required
def reminder_list_create(request, medicine_pk):
    # ... (Implementation for listing and creating reminders for a specific medicine)
    return JsonResponse({'message': 'Endpoint for reminders.'})

# --- Agent Logic Placeholder ---

@csrf_exempt
@login_required
def trigger_reminders(request):
    """
    This is where the core AGENT logic for PS1 will go.
    This endpoint would be called by a scheduler (e.g., Celery Beat, cron job).
    """
    # 1. Find all active reminders that are due.
    # 2. Send interactive notifications (email, push, SMS).
    # 3. Check medicine inventory and trigger refill alerts.
    
    print("AGENT LOGIC: Checking and sending medication reminders...")
    
    return JsonResponse({'status': 'Reminder check initiated.'})