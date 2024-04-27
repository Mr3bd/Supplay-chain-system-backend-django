import random
import string
from .models import User

supplier_modules = ['addMaterial', 'getMaterials']
manufacture_modules = ['addProduct','getAvailableMaterials', 'addProduct', 'getProducts']

def check_permission(log_id, module = None, log_data = None):
    if log_id is None:
            print('h1')
            return False
    if log_data is None:
        print('h2')
        user = User.objects.get(id=log_id)
    else:
          user = log_data
    if user.role.id == 1:
        print('h3')
        return True
    elif module is None:
          print('h4')
          return False
    elif user.role.id == 2 and module in supplier_modules:
        print('h5')
        return True
    elif user.role.id == 3 and module in manufacture_modules:
        print('h6')   
        return True
    

    return False



def generate_batch_id():
    characters = string.ascii_uppercase + string.digits
    batch_id = ''.join(random.choice(characters) for _ in range(10))
    return batch_id