from django.http import JsonResponse
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from .models import User, Role, Material
import json
from .methods import check_permission

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('id')
        print(user_id)
        if user_id is None:
            return JsonResponse({'error': 'ID not provided'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            if user.deleted == 0:
                user_dict = model_to_dict(user)
                user_dict['role_info'] = user.get_role_info()
                return JsonResponse({'user': user_dict})
            else:
                 return JsonResponse({'error': 'User Deleted'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def addUser(request):
    from datetime import datetime
    current_datetime = datetime.now()
    if request.method == 'POST':
        data = json.loads(request.body)
        log_id = data.get('log_id')
        has_per = check_permission(log_id, 'addUser')
        if has_per:
            user_id = data.get('id')
            name = data.get('name')
            role = data.get('role')
            logtime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

            if None in (user_id, name, role):
                return JsonResponse({'error': 'Incomplete data provided'}, status=400)

            try:
                role_model = Role.objects.get(id=role)
                # Create a new user instance and save it to the database
                User.objects.create(id = user_id, name = name, role = role_model, deleted = 0, logtime = logtime)
                return JsonResponse({'success': 'User added successfully'})
            except Exception as e:
                print(e)
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def deleteUser(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        log_id = data.get('log_id')
        has_per = check_permission(log_id, 'addUser')
        if has_per:
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
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def activateUser(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        log_id = data.get('log_id')
        has_per = check_permission(log_id, 'addUser')
        if has_per:
            user_id = data.get('id')
            if user_id is None:
                return JsonResponse({'error': 'ID not provided'}, status=400)

            try:
                # Get the user by ID and update the 'deleted' field
                user = User.objects.get(id=user_id)
                user.deleted = 0
                user.save()
                return JsonResponse({'success': 'User deleted successfully'})
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def rolesLookUp(request):
    if request.method == 'GET':
        roles = Role.objects.all().order_by('id')

        # Get page number and page size from query parameters
        page_number = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('pageSize', 5))

        paginator = Paginator(roles, page_size)

        try:
            page = paginator.page(page_number)
            role_list = list(page.object_list.values())
            return JsonResponse({'roles': role_list})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def getMaterials(request):
    if request.method == 'GET':
        log_id = request.GET.get('log_id')
        has_per = check_permission(log_id, 'getMaterials')
   
        if has_per:
            materials = Material.objects.all().order_by('-logtime')

            # Get page number and page size from query parameters
            page_number = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('pageSize', 5))

            paginator = Paginator(materials, page_size)

            try:
                page = paginator.page(page_number)
                materials_list = list(page.object_list.values())
                return JsonResponse({'materials': materials_list})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def getUsers(request):
    if request.method == 'GET':
        log_id = request.GET.get('log_id')
        has_per = check_permission(log_id,)
   
        if has_per:
            users = User.objects.all().order_by('role')

            # Get page number and page size from query parameters
            page_number = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('pageSize', 5))

            paginator = Paginator(users, page_size)

            try:
                page = paginator.page(page_number)
                users_list = []
                for user in page.object_list:
                    user_data = model_to_dict(user)
                    user_data['role_info'] = user.get_role_info()  # Include role info
                    users_list.append(user_data)
                return JsonResponse({'users': users_list})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def addMaterial(request):
    from datetime import datetime
    current_datetime = datetime.now()
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        log_id = data.get('log_id')
        has_per = check_permission(log_id, 'addMaterial')
        if has_per:
            trans_id = data.get('trans_id')
            owner_user = User.objects.get(id=log_id)
            name = data.get('name')
            quantity = data.get('quantity')
            price = data.get('price')
            logtime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

            if None in (trans_id, name, quantity):
                return JsonResponse({'error': 'Incomplete data provided'}, status=400)

            try:
                # Create a new user instance and save it to the database
                Material.objects.create(trans_id = trans_id, name = name, quantity = quantity, owner = owner_user, logtime = logtime, price = price)
                return JsonResponse({'success': 'Material added successfully'})
            except Exception as e:
                print(str(e))
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def changeUserRole(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        log_id = data.get('log_id')
        has_per = check_permission(log_id, 'changeRole')
        if has_per:
            user_id = data.get('id')
            role_id = data.get('role_id')
            if user_id is None:
                return JsonResponse({'error': 'ID not provided'}, status=400)
            try:
                # Get the user by ID and update the 'deleted' field
                user = User.objects.get(id=user_id)
                user.role = Role.objects.get(id=role_id) 
                user.save()
                return JsonResponse({'success': 'User role updated successfully'})
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            except Exception as e:
                print(e)
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)