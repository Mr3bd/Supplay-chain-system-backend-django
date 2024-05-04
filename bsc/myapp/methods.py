import random
import string
from .models import User

supplier_modules = ['addMaterial', 'getMaterials']
manufacture_modules = ['addProduct','getAvailableMaterials',
                       'addProduct', 'getProducts', 'getUsersByFilter',
                       'createQaRequest', 'sendOrderForShipping']
qa_modules = ['getQARequests', 'acceptQaRequest', 'completeQaRequest']
logistics_modules = ['getShippingRequests', 'acceptShippingRequest', 'completeShippingRequest']
retailer_modules = ['getStoreProducts', 'addOrder', 'createShippingRequest']

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
    elif user.role.id == 4 and module in qa_modules:
        print('h7')   
        return True    
    
    elif user.role.id == 6 and module in retailer_modules:
        print('h7')   
        return True    
    return False



def generate_batch_id():
    characters = string.ascii_uppercase + string.digits
    batch_id = ''.join(random.choice(characters) for _ in range(10))
    return batch_id


def generate_shippment_id():
    characters = string.ascii_uppercase + string.digits
    shippment_id = ''.join(random.choice(characters) for _ in range(10))
    return shippment_id