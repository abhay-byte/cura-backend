# reminder_agent/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Medicine, Reminder

# Helper to check ownership
def is_owner(user, model_instance):
    # For Reminder instances, check ownership through the medicine
    if hasattr(model_instance, 'medicine'):
        return user == model_instance.medicine.user
    return user == model_instance.user

# --- Medicine Endpoints ---

@csrf_exempt
@login_required
def medicine_list_create(request):
    if request.method == 'GET':
        medicines = Medicine.objects.filter(user=request.user)
        data = []
        for med in medicines:
            reminders_data = [{
                'id': rem.id,
                'time': rem.reminder_time.strftime('%H:%M'),
                'quantity': rem.quantity,
                'instruction': rem.instruction
            } for rem in med.reminders.all()]
            
            data.append({
                'id': med.id,
                'name': med.name,
                'dosage': med.dosage,
                'inventory': med.inventory,
                'reminders': reminders_data
            })
        return JsonResponse(data, safe=False)

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

    if request.method == 'GET':
        # ... (This can be expanded if needed, but list view is more comprehensive)
        return JsonResponse({'id': medicine.id, 'name': medicine.name})
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            medicine.name = data.get('name', medicine.name)
            medicine.dosage = data.get('dosage', medicine.dosage)
            medicine.inventory = data.get('inventory', medicine.inventory)
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
def reminder_create(request, medicine_pk):
    try:
        medicine = Medicine.objects.get(pk=medicine_pk)
        if not is_owner(request.user, medicine):
            return JsonResponse({'error': 'Not authorized.'}, status=403)
    except Medicine.DoesNotExist:
        return JsonResponse({'error': 'Medicine not found.'}, status=404)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reminder = Reminder.objects.create(
                medicine=medicine,
                reminder_time=data['time'],
                quantity=data.get('quantity', 1),
                instruction=data.get('instruction', 'Any Time')
            )
            return JsonResponse({'message': 'Reminder added successfully.', 'reminder_id': reminder.id}, status=201)
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data.'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@login_required
def take_medicine(request, reminder_pk):
    try:
        reminder = Reminder.objects.get(pk=reminder_pk)
        if not is_owner(request.user, reminder):
            return JsonResponse({'error': 'Not authorized.'}, status=403)
    except Reminder.DoesNotExist:
        return JsonResponse({'error': 'Reminder not found.'}, status=404)

    if request.method == 'POST':
        medicine = reminder.medicine
        quantity_to_take = reminder.quantity

        if medicine.inventory < quantity_to_take:
            return JsonResponse({'error': 'Not enough medicine in inventory.'}, status=400)

        medicine.inventory -= quantity_to_take
        medicine.save()

        return JsonResponse({
            'message': f'Recorded that you took {medicine.name}.',
            'new_inventory': medicine.inventory
        })

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)



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