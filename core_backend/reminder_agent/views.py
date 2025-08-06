# reminder_agent/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import requests # Import the requests library
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

# --- Agent Logic Placeholder (UPDATED) ---

@csrf_exempt
@login_required # Or remove this if the cron job will call it without a session
def trigger_reminders(request):
    """
    This endpoint acts as a trigger. It calls the separate Flask-based
    reminder agent service to perform the actual work of sending emails.
    """
    # The URL where the Flask reminder agent is running
    reminder_agent_url = "http://127.0.0.1:5000/api/reminder/trigger/"
    
    print(f"Forwarding request to reminder agent at: {reminder_agent_url}")

    try:
        # Make a GET request to the Flask agent
        response = requests.get(reminder_agent_url, timeout=60) # 60-second timeout
        
        # Check if the agent responded successfully
        if response.status_code == 200:
            # Return the response from the agent directly to the client
            agent_response_data = response.json()
            print(f"Agent responded successfully: {agent_response_data}")
            return JsonResponse(agent_response_data)
        else:
            # Handle cases where the agent returns an error
            error_message = f"Reminder agent failed with status code {response.status_code}: {response.text}"
            print(error_message)
            return JsonResponse({'error': error_message}, status=502) # 502 Bad Gateway

    except requests.exceptions.RequestException as e:
        # Handle network errors (e.g., the agent service is down)
        error_message = f"Could not connect to the reminder agent: {e}"
        print(error_message)
        return JsonResponse({'error': error_message}, status=503) # 503 Service Unavailable
