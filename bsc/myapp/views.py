from django.http import JsonResponse
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from .models import User, Role, Material, Product, OrderStatus, ProductMaterial, QaStatus, QaRequest, Order, ShippingRequest, ShippingStatus, SystemLog, Notification
import json
from .methods import check_permission, generate_batch_id, generate_shippment_id, getPermissionByRole
from django.db.models import Q

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
                user_dict['permissions'] = getPermissionByRole(user.role)
                unopened_notification_count = Notification.objects.filter(noti_user = user, opened=0).count()
                user_dict['unReadNoti'] = unopened_notification_count

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
            material_id = data.get('material_id')
            owner_user = User.objects.get(id=log_id)
            name = data.get('name')
            quantity = data.get('quantity')
            price = data.get('price')
            logtime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

            if None in (trans_id, name, quantity, material_id):
                return JsonResponse({'error': 'Incomplete data provided'}, status=400)

            try:
                # Create a new user instance and save it to the database
                Material.objects.create(trans_id = trans_id, name = name, material_id = material_id, quantity = quantity, owner = owner_user, logtime = logtime, price = price)
                log_action(trans_id=trans_id, owner=owner_user, description='Added a material', logtime=logtime )

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



@csrf_exempt
def getAvailableMaterials(request):
    if request.method == 'GET':
        log_id = request.GET.get('log_id')
        has_per = check_permission(log_id, 'getAvailableMaterials')
   
        if has_per:
            materials = Material.objects.filter(quantity__gt=0).order_by('-logtime')

            if materials.exists():  # Check if queryset is not empty
                return JsonResponse({'materials': list(materials.values())})
            else:
                return JsonResponse({'materials': []})  # Return empty string if materials queryset is empty
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def getUsersByFilter(request):
    if request.method == 'GET':
        log_id = request.GET.get('log_id')
        role_id = request.GET.get('role_id')
        has_per = check_permission(log_id, 'getUsersByFilter')
   
        if has_per:
            role = Role.objects.get(id=role_id)

            users = User.objects.filter(role=role, deleted = 0).order_by('-logtime')

            if users.exists():  # Check if queryset is not empty
                return JsonResponse({'users': list(users.values())})
            else:
                return JsonResponse({'users': []})  # Return empty string if materials queryset is empty
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
def addProduct(request):
    from datetime import datetime
    current_datetime = datetime.now()
    if request.method == 'POST':
        data = json.loads(request.body)
        log_id = data.get('log_id')
        has_per = check_permission(log_id, 'addProduct')
        if has_per:
            trans_id = data.get('trans_id')
            product_id = data.get('product_id')
            owner_user = User.objects.get(id=log_id)
            name = data.get('name')
            quantity = data.get('quantity')
            price = data.get('price')
            status_id = 4
            batch_id = generate_batch_id()
            material_ids_json = data.get('material_ids')
            logtime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            
            if None in (trans_id, name, quantity, price,  material_ids_json, product_id):
                return JsonResponse({'error': 'Incomplete data provided'}, status=400)

            try:
                print('here')
                # Create a new user instance and save it to the database
                status_model = OrderStatus.objects.get(id=status_id)
                product = Product.objects.create(trans_id = trans_id, batch_id = batch_id, product_id = product_id, owner = owner_user, status = status_model, name = name,  quantity = quantity,  price = price, logtime = logtime)
                material_ids = json.loads(material_ids_json)

                for material_data in material_ids:
                    print('for loop')
                    material_id = material_data['id']
                    qty = material_data['quantity']
                    material = Material.objects.get(pk=material_id)

                    # Subtract quantity from material record
                    material.quantity -= qty
                    if material.quantity == 0:
                        noti_action(noti_users = [material.owner], description= 'Your material is out of stock', logtime=logtime)

                    material.save()
                    ProductMaterial.objects.create(product=product, material=material, quantity=qty)
                    log_action(trans_id=trans_id, owner=owner_user, description='Added a product', logtime=logtime )

                return JsonResponse({'success': 'Product added successfully'})
            except Exception as e:
                print('error e')
                print(str(e))
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
def getProducts(request):
    if request.method == 'GET':
        log_id = request.GET.get('log_id')
        has_per = check_permission(log_id, 'getProducts')
   
        if has_per:
            products = Product.objects.all().order_by('-logtime')

            # Get page number and page size from query parameters
            page_number = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('pageSize', 5))

            paginator = Paginator(products, page_size)

            try:
                page = paginator.page(page_number)
                products_list = []
                for product in page.object_list:
                    product_data = model_to_dict(product)
                    product_data['owner_info'] = product.get_owner_info()
                    product_data['status_info'] = product.get_status_info()
                    products_list.append(product_data)

                return JsonResponse({'products': products_list})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
def createQaRequest(request):
    from datetime import datetime
    current_datetime = datetime.now()
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        log_id = data.get('log_id')
        has_per = check_permission(log_id, 'createQaRequest')
        if has_per:
            trans_id = data.get('trans_id')
            product_id = data.get('product_id')
            reward = data.get('reward')
            item_count = data.get('item_count')

            status_id = 1
            logtime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            print(logtime)            
            if None in (trans_id, product_id, reward, status_id):
                return JsonResponse({'error': 'Incomplete data provided'}, status=400)

            try:
                print('check')
                # qa_user = User.objects.get(id=qa_id)
                status_model = QaStatus.objects.get(id=status_id)
                product = Product.objects.get(pk=product_id)
                QaRequest.objects.create(trans_id = trans_id, product = product, status = status_model, item_count = item_count, reward = reward, logtime = logtime)
                p_status = OrderStatus.objects.get(id=9)
                product.status = p_status
                product.save()
                log_action(trans_id=trans_id, owner=product.owner, description='Requested a product review', logtime=logtime )
                role = Role.objects.get(id=4)
                noti_users = User.objects.filter(role=role)
                noti_action(noti_users = noti_users, description= 'There is a new QA request', logtime=logtime)
                return JsonResponse({'success': 'Request added successfully'})
            except Exception as e:
                print('error e')
                print(str(e))
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)




@csrf_exempt
def getQARequests(request):
    if request.method == 'GET':
        log_id = request.GET.get('log_id')
        has_per = check_permission(log_id, 'getQARequests')
   
        if has_per:
            qa_requests = QaRequest.objects.all().order_by('-logtime')

            # Get page number and page size from query parameters
            page_number = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('pageSize', 5))

            paginator = Paginator(qa_requests, page_size)

            try:
                page = paginator.page(page_number)
                requests = []
                for request in page.object_list:
                    request_data = model_to_dict(request)
                    request_data['status_info'] = request.get_status_info()
                    request_data['product_info'] = request.get_product_info()
                    requests.append(request_data)

                return JsonResponse({'requests': requests})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def acceptQaRequest(request):
    from datetime import datetime
    current_datetime = datetime.now()
    if request.method == 'POST':
        data = json.loads(request.body)
        log_id = data.get('log_id')
        has_per = check_permission(log_id, 'acceptQaRequest')
        if has_per:
            request_id = data.get('request_id')
            product_id = data.get('product_id')
            rstatus_id = 2
            pstatus_id = 8

            # used for logger
            trans_id = data.get('trans_id')
            logtime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

            if None in (trans_id, request_id, product_id, logtime):
                return JsonResponse({'error': 'Incomplete data provided'}, status=400)

            try:
                qa_user = User.objects.get(id=log_id)
                status_model = QaStatus.objects.get(id=rstatus_id)
                
                qaRequest = QaRequest.objects.get(pk=request_id)
                qaRequest.qa = qa_user
                qaRequest.status = status_model
                qaRequest.save()

                product = Product.objects.get(pk=product_id)
                pstatus_model = OrderStatus.objects.get(id=pstatus_id)
                product.status = pstatus_model
                product.save()                
                log_action(trans_id=trans_id, owner=qa_user, description='Accepted the request to review a product', logtime=logtime )
                noti_action(noti_users = [product.owner], description= 'A QA user has accepted your request to review your product', logtime=logtime)
                return JsonResponse({'success': 'Request accepted successfully'})
            except Exception as e:
                print('error e')
                print(str(e))
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
def completeQaRequest(request):
    from datetime import datetime
    current_datetime = datetime.now()
    if request.method == 'POST':
        data = json.loads(request.body)
        log_id = data.get('log_id')
        has_per = check_permission(log_id, 'completeQaRequest')
        if has_per:
            request_id = data.get('request_id')
            product_id = data.get('product_id')
            rstatus_id = 3
            pstatus_id = data.get('product_status')

            # used for logger
            trans_id = data.get('trans_id')
            logtime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

            if None in (trans_id, request_id, product_id, logtime):
                return JsonResponse({'error': 'Incomplete data provided'}, status=400)

            try:
                status_model = QaStatus.objects.get(id=rstatus_id)

                qaRequest = QaRequest.objects.get(pk=request_id)
                qaRequest.status = status_model
                qaRequest.save()

                product = Product.objects.get(pk=product_id)
                pstatus_model = OrderStatus.objects.get(id=pstatus_id)
                product.status = pstatus_model
                product.save()                
                log_action(trans_id=trans_id, owner=qaRequest.qa, description='Completed the product review', logtime=logtime )

                if pstatus_id == 3:
                    noti_action(noti_users = [product.owner], description= 'A QA user has completed a review of your product and your product has failed the test', logtime=logtime)
                else:
                    noti_action(noti_users = [product.owner], description= 'The QA user has completed reviewing your product and your product has been successfully tested, your product is now in-stock', logtime=logtime)

                return JsonResponse({'success': 'Request completed successfully'})
            except Exception as e:
                print('error e')
                print(str(e))
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def cancelQaRequest(request):
    from datetime import datetime
    current_datetime = datetime.now()
    if request.method == 'POST':
        data = json.loads(request.body)
        log_id = data.get('log_id')
        request_id = data.get('request_id')
        trans_id = data.get('trans_id')
        if None in (log_id, request_id):
            return JsonResponse({'error': 'Incomplete data provided'}, status=400)
        
        qaRequest = QaRequest.objects.filter(trans_id=request_id).order_by('-logtime').first()
        if qaRequest:
            product = Product.objects.get(pk=qaRequest.product.trans_id)
            has_per = product.owner.id == log_id
            logtime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            if has_per:
                try:                    
                    newStatus = QaStatus.objects.get(id=4)
                    qaRequest.status = newStatus
                    qaRequest.save()

                    pstatus = OrderStatus.objects.get(id=4)
                    product.status = pstatus
                    product.save()                
                    log_action(trans_id=trans_id, owner=product.owner, description='Canceled the request to review the product', logtime=logtime )
                    return JsonResponse({'success': 'Request canceled successfully'})
                except Exception as e:
                    print('error e')
                    print(str(e))
                    return JsonResponse({'error': str(e)}, status=500)
            else:
                return JsonResponse({'error': 'Unauthorized'}, status=401)
        else:
            return JsonResponse({'error': 'Item not found'}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

def getQaRequest(request):
    if request.method == 'GET':
        log_id = request.GET.get('log_id')
        product_id = request.GET.get('product_id')
        req_status = request.GET.get('status')
        if None in (log_id, product_id, req_status):
            return JsonResponse({'error': 'Incomplete data provided'}, status=400)
        
        product = Product.objects.get(pk=product_id)
        has_per = product.owner.id == log_id
        if has_per:
            currentStatus = QaStatus.objects.get(id=req_status)
            qaRequest = QaRequest.objects.filter(
                    product_id=product_id, 
                    status=currentStatus).order_by('-logtime').first()
            if qaRequest:
                request_data = {
                    'trans_id': qaRequest.trans_id,
                    'item_count': qaRequest.item_count,
                    'reward': qaRequest.reward,
                }
                return JsonResponse({'request_data': request_data})
            else:
                return JsonResponse({'error': 'Request not found'})

        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
   
   
@csrf_exempt
def getStoreProducts(request):
    if request.method == 'GET':
        log_id = request.GET.get('log_id')
        has_per = check_permission(log_id, 'getStoreProducts')
   
        if has_per:
            statusIn_model = OrderStatus.objects.get(id=1)
            statusOut_model = OrderStatus.objects.get(id=2)
            products = Product.objects.filter(
                status__in=[statusIn_model, statusOut_model]).order_by('-logtime')
            #quantity__gt=0
            # Get page number and page size from query parameters
            page_number = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('pageSize', 5))

            paginator = Paginator(products, page_size)

            try:
                page = paginator.page(page_number)
                products_list = []
                for product in page.object_list:
                    product_data = model_to_dict(product)
                    product_data['owner_info'] = product.get_owner_info()
                    product_data['status_info'] = product.get_status_info()
                    products_list.append(product_data)

                return JsonResponse({'products': products_list})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)




@csrf_exempt
def addOrder(request):
    from datetime import datetime
    current_datetime = datetime.now()
    if request.method == 'POST':
        data = json.loads(request.body)
        log_id = data.get('log_id')
        has_per = check_permission(log_id, 'addOrder')
        if has_per:
            trans_id = data.get('trans_id')            
            quantity = data.get('quantity')
            product_id = data.get('product_id')
            item_count = data.get('item_count')
            
            if None in (trans_id, quantity, product_id, item_count):
                return JsonResponse({'error': 'Incomplete data provided'}, status=400)
            
            try:
                logtime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                owner_user = User.objects.get(id=log_id)
                status_model = OrderStatus.objects.get(id=5)
                product = Product.objects.get(trans_id=product_id)

   
                if product.quantity - quantity >= 0:
                    Order.objects.create(trans_id = trans_id, product = product, owner = owner_user, item_count = item_count, status = status_model, quantity = quantity, logtime = logtime)
                    product.quantity -= quantity
                    if product.quantity == 0:
                        noti_action(noti_users = [product.owner], description= 'Your product is out of stock', logtime=logtime)
                        product.status = OrderStatus.objects.get(id=2)
                    product.save()  
                    log_action(trans_id=trans_id, owner=owner_user, description='Added an order', logtime=logtime )
                    noti_action(noti_users = [product.owner], description= 'Someone has purchased your product', logtime=logtime)
                    return JsonResponse({'success': 'Product added successfully'})
                else:
                    return JsonResponse({'Invalid quantity': str(e)}, status=500)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def getOrders(request):
    if request.method == 'GET':
        log_id = request.GET.get('log_id')
        has_per = check_permission(log_id, 'getOrders')
   
        if has_per:
            orders = Order.objects.all()
            #quantity__gt=0
            # Get page number and page size from query parameters
            page_number = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('pageSize', 5))

            paginator = Paginator(orders, page_size)

            try:
                page = paginator.page(page_number)
                orders_list = []
                for order in page.object_list:
                    order_data = model_to_dict(order)
                    order_data['status_info'] = order.get_status_info()
                    order_data['product_info'] = order.get_product_info()
                    order_data['requester_info'] = order.get_requester_info()
                    orders_list.append(order_data)

                return JsonResponse({'orders': orders_list})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)




@csrf_exempt
def sendOrderForShipping(request):
    from datetime import datetime
    current_datetime = datetime.now()
    if request.method == 'POST':
        data = json.loads(request.body)
        log_id = data.get('log_id')
        trans_id = data.get('trans_id')
        has_per = check_permission(log_id, 'sendOrderForShipping')
        if has_per:
            order_id = data.get('order_id')
            
            if order_id is None :
                return JsonResponse({'error': 'Incomplete data provided'}, status=400)
            
            try:
                status_model = OrderStatus.objects.get(id=10)
                order = Order.objects.get(trans_id=order_id)
                logtime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                if order.product.owner.id == log_id:
                    order.status = status_model
                    order.save()  
                    log_action(trans_id=trans_id, owner=order.product.owner, description='Sent the product for shipping', logtime=logtime )
                    noti_action(noti_users = [order.product.owner], description= 'The manufacturer has completed packaging your order and is now ready to ship', logtime=logtime)

                    return JsonResponse({'success': 'Successfully'})
                else:
                    return JsonResponse({'error': 'Unauthorized'}, status=401)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def createShippingRequest(request):
    from datetime import datetime
    current_datetime = datetime.now()
    if request.method == 'POST':
        data = json.loads(request.body)
        log_id = data.get('log_id')
        has_per = check_permission(log_id, 'createShippingRequest')
        if has_per:
            trans_id = data.get('trans_id')
            order_id = data.get('order_id')
            reward = data.get('reward')
            item_count = data.get('item_count')

            status_id = 1
            logtime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            if None in (trans_id, order_id, reward, status_id):
                return JsonResponse({'error': 'Incomplete data provided'}, status=400)

            try:
                status_model = ShippingStatus.objects.get(id=status_id)
                order = Order.objects.get(pk=order_id)
                ShippingRequest.objects.create(trans_id = trans_id, product_order = order, status = status_model, item_count = item_count, reward = reward, logtime = logtime)
                o_status = OrderStatus.objects.get(id=11)
                order.status = o_status
                order.save()
                log_action(trans_id=trans_id, owner=order.owner, description='Sent a request to ship the order', logtime=logtime )
                role = Role.objects.get(id=5)
                noti_users = User.objects.filter(role=role)
                
                noti_action(noti_users = noti_users, description= 'There is a new Shipping request', logtime=logtime)

                return JsonResponse({'success': 'Request added successfully'})
            except Exception as e:
                print('error e')
                print(str(e))
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def getShippingRequests(request):
    if request.method == 'GET':
        log_id = request.GET.get('log_id')
        has_per = check_permission(log_id, 'getShippingRequests')
   
        if has_per:
            shipping_requests = ShippingRequest.objects.all().order_by('-logtime')

            # Get page number and page size from query parameters
            page_number = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('pageSize', 5))

            paginator = Paginator(shipping_requests, page_size)

            try:
                page = paginator.page(page_number)
                requests = []
                for req in page.object_list:
                    request_data = model_to_dict(req)
                    request_data['status_info'] = req.get_status_info()
                    request_data['order_info'] = req.get_order_info()
                    requests.append(request_data)

                return JsonResponse({'requests': requests})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def acceptShippingRequest(request):
    from datetime import datetime
    current_datetime = datetime.now()
    if request.method == 'POST':
        data = json.loads(request.body)
        log_id = data.get('log_id')
        has_per = check_permission(log_id, 'acceptShippingRequest')
        if has_per:
            request_id = data.get('request_id')
            order_id = data.get('order_id')
            rstatus_id = 2
            ostatus_id = 6

            # used for logger
            trans_id = data.get('trans_id')
            logtime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

            if None in (trans_id, request_id, order_id, logtime):
                return JsonResponse({'error': 'Incomplete data provided'}, status=400)

            try:
                lg_user = User.objects.get(id=log_id)
                status_model = ShippingStatus.objects.get(id=rstatus_id)
                shippment_id = generate_shippment_id()

                shippingRequest = ShippingRequest.objects.get(pk=request_id)
                shippingRequest.lg = lg_user
                shippingRequest.status = status_model
              
                shippingRequest.save()

                order = Order.objects.get(pk=order_id)
                ostatus_model = OrderStatus.objects.get(id=ostatus_id)
                order.shipment_id = shippment_id
                order.status = ostatus_model
                order.save()                
                log_action(trans_id=trans_id, owner=lg_user, description='Accepted the request to ship an order', logtime=logtime )
                noti_action(noti_users = [order.owner], description= 'A Delivery Specialist user has accepted your request to ship your order', logtime=logtime)

                return JsonResponse({'success': 'Request accepted successfully'})
            except Exception as e:
                print('error e')
                print(str(e))
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def completeShippingRequest(request):
    from datetime import datetime
    current_datetime = datetime.now()
    if request.method == 'POST':
        data = json.loads(request.body)
        log_id = data.get('log_id')
        has_per = check_permission(log_id, 'completeShippingRequest')
        if has_per:
            request_id = data.get('request_id')
            order_id = data.get('order_id')
            rstatus_id = 3
            ostatus_id = 7

            # used for logger
            trans_id = data.get('trans_id')
            logtime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

            if None in (trans_id, request_id, order_id):
                return JsonResponse({'error': 'Incomplete data provided'}, status=400)

            try:
                status_model = ShippingStatus.objects.get(id=rstatus_id)

                shippingRequest = ShippingRequest.objects.get(pk=request_id)
                shippingRequest.status = status_model
                shippingRequest.save()

                order = Order.objects.get(pk=order_id)
                ostatus_model = OrderStatus.objects.get(id=ostatus_id)
                order.status = ostatus_model
                order.save()                
                log_action(trans_id=trans_id, owner=shippingRequest.lg, description='Completed shipping the order', logtime=logtime )
                noti_action(noti_users = [order.owner], description= 'A Delivery Specialist user has completed shipping your order', logtime=logtime)

                return JsonResponse({'success': 'Request completed successfully'})
            except Exception as e:
                print('error e')
                print(str(e))
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def cancelShippingRequest(request):
    from datetime import datetime
    current_datetime = datetime.now()
    if request.method == 'POST':
        data = json.loads(request.body)
        log_id = data.get('log_id')
        request_id = data.get('request_id')
        trans_id = data.get('trans_id')
        if None in (log_id, request_id):
            return JsonResponse({'error': 'Incomplete data provided'}, status=400)
        
        shippingRequest = ShippingRequest.objects.filter(trans_id=request_id).order_by('-logtime').first()
        if shippingRequest:
            order = Order.objects.get(pk=shippingRequest.product_order.trans_id)
            has_per = order.owner.id == log_id
            if has_per:
                try:                    
                    logtime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
                    newStatus = ShippingStatus.objects.get(id=4)
                    shippingRequest.status = newStatus
                    shippingRequest.save()

                    ostatus = OrderStatus.objects.get(id=10)
                    order.status = ostatus
                    order.save()                
                    log_action(trans_id=trans_id, owner=order.owner, description='Canceled the order shipping request', logtime=logtime )

                    return JsonResponse({'success': 'Request canceled successfully'})
                except Exception as e:
                    print('error e')
                    print(str(e))
                    return JsonResponse({'error': str(e)}, status=500)
            else:
                return JsonResponse({'error': 'Unauthorized'}, status=401)
        else:
            return JsonResponse({'error': 'Item not found'}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def getShippingRequest(request):
    if request.method == 'GET':
        log_id = request.GET.get('log_id')
        order_id = request.GET.get('order_id')
        req_status = request.GET.get('status')
        if None in (log_id, order_id, req_status):
            return JsonResponse({'error': 'Incomplete data provided'}, status=400)
        
        order = Order.objects.get(pk=order_id)
        has_per = order.owner.id == log_id
        if has_per:
            currentStatus = ShippingStatus.objects.get(id=req_status)
            shippingRequest = ShippingRequest.objects.filter(
                    product_order=order, 
                    status=currentStatus).order_by('-logtime').first()
            if shippingRequest:
                request_data = {
                    'trans_id': shippingRequest.trans_id,
                    'item_count': shippingRequest.item_count,
                    'reward': shippingRequest.reward,
                }
                return JsonResponse({'request_data': request_data})
            else:
                return JsonResponse({'error': 'Request not found'})

        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
def getSystemLogs(request):
    if request.method == 'GET':
        log_id = request.GET.get('log_id')
        has_per = check_permission(log_id, 'getSystemLogs')
   
        if has_per:
            system_logs = SystemLog.objects.all().order_by('-logtime')

            # Get page number and page size from query parameters
            page_number = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('pageSize', 5))

            paginator = Paginator(system_logs, page_size)

            try:
                page = paginator.page(page_number)
                logs = []
                for log in page.object_list:
                    log_data = model_to_dict(log)
                    log_data['owner_info'] = log.get_owner_info()
                    logs.append(log_data)

                return JsonResponse({'logs': logs})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def getNotifications(request):
    if request.method == 'GET':
        log_id = request.GET.get('log_id')
        has_per = check_permission(log_id, 'getNotifications')
   
        if has_per:
            user = User.objects.get(id=log_id)
            notifications = Notification.objects.filter(noti_user = user).order_by('-logtime')

            # Get page number and page size from query parameters
            page_number = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('pageSize', 5))

            paginator = Paginator(notifications, page_size)

            try:
                page = paginator.page(page_number)
                notis = []
                for noti in page.object_list:
                    noti.opened = 1
                    noti.save()
                    notis.append(model_to_dict(noti))
                unopened_notification_count = Notification.objects.filter(noti_user = user, opened=0).count()

                return JsonResponse({'notifications': notis, 'unReadNoti': unopened_notification_count})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def log_action(trans_id, owner, description, logtime):
        SystemLog.objects.create(trans_id = trans_id, owner = owner, description = description, logtime = logtime)

def noti_action(noti_users, description, logtime):
        for u in noti_users:
            Notification.objects.create(noti_user = u, description = description, opened = 0, logtime = logtime)
