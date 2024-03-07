from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('id')

        if user_id is None:
            return JsonResponse({'error': 'ID not provided'}, status=400)

        try:
            # You can customize the data returned as per your requirement
            # return JsonResponse({'user': {
            #     'id': user.id,
            #     # Add other fields here
            # }})

            user = User.objects.get(id=user_id)
            # Convert the user instance to dictionary
            if user.delete == 0:
                user_dict = model_to_dict(user)
                return JsonResponse({'user': user_dict})
            else:
                 return JsonResponse({'error': 'User Deleted'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def addUser(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('id')
        name = data.get('name')
        role = data.get('role')

        if None in (user_id, name, role):
            return JsonResponse({'error': 'Incomplete data provided'}, status=400)

        try:
            # Create a new user instance and save it to the database
            User.objects.create(id=user_id, name=name, role=role, deleted = 0)
            return JsonResponse({'success': 'User added successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def deleteUser(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('id')

        if user_id is None:
            return JsonResponse({'error': 'ID not provided'}, status=400)

        try:
            # Get the user by ID and update the 'deleted' field
            user = User.objects.get(id=user_id)
            user.deleted = 1
            user.save()
            return JsonResponse({'success': 'User deleted successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)