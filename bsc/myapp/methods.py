from .models import User
supplier_modules = ['addMaterial']
manufacture_modules = ['addProduct']

def check_permission(log_id, module, log_data = None):
    if None in (log_id, module):
            return False
    if log_data is None:
        user = User.objects.get(id=log_id)
    else:
          user = log_data
    if user.role == 1:
        return True
    elif user.role == 2 and module in supplier_modules:
        return True
    elif user.role == 3 and module in manufacture_modules:
        return True

    return False