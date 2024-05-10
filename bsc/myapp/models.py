from django.db import models

class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'Roles'
        ordering = ['id']  # Order by id ascending

class User(models.Model):
    id = models.CharField(primary_key=True, max_length=64, db_index=True)
    name = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, db_column='role')
    deleted = models.IntegerField()
    logtime = models.CharField(max_length=255)
    class Meta:
        db_table = 'Users'

    def get_role_info(self):
        if self.role:
            return {
                'role_id': self.role.id,
                'role_name': self.role.name
            }
        else:
            return None


class Material(models.Model):
    trans_id = models.CharField(primary_key=True, max_length=70)
    quantity = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='owner')  # Foreign key relationship to User table
    logtime = models.CharField(max_length=255)
    name = models.CharField(max_length=255)  # New column
    price = models.FloatField()
    material_id = models.CharField(max_length=255, null=True)  # Add the status field

    class Meta:
        db_table = 'Materials'
        ordering = ['-logtime']


class OrderStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'OrderStatusLookup'
        ordering = ['id']  # Order by id ascending

class Product(models.Model):
    trans_id = models.CharField(primary_key=True, max_length=70)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='owner_id')  # Foreign key relationship to User table
    logtime = models.CharField(max_length=255)
    name = models.CharField(max_length=255)  # New column
    price = models.FloatField()
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True, db_column='status_id')
    batch_id = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255, null=True)  # Add the status field
    quantity = models.IntegerField()
    
    class Meta:
        db_table = 'Products'
        ordering = ['-logtime']

    def get_status_info(self):
        if self.status:
            return {
                'status_id': self.status.id,
                'status_name': self.status.name
            }
        else:
            return None
    def get_owner_info(self):
        if self.owner:
            return {
                'owner_id': self.owner.id,
                'owner_name': self.owner.name
            }
        else:
            return None
        
class ProductMaterial(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    class Meta:
        db_table = 'ProductMaterial'
        ordering = ['-quantity']


class QaStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'QA_Status'
        ordering = ['id']  # Order by id ascending


class ShippingStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ShippingStatus'
        ordering = ['id']  # Order by id ascending


class QaRequest(models.Model):
    trans_id = models.CharField(primary_key=True, max_length=70)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')
    qa = models.ForeignKey(User, on_delete=models.CASCADE, db_column='qa')
    reward = models.FloatField()
    status = models.ForeignKey(QaStatus, on_delete=models.SET_NULL, null=True, db_column='status')
    logtime = models.CharField(max_length=255)
    item_count = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'QA_Requests'
        ordering = ['-logtime']
        
    def get_status_info(self):
        if self.status:
            return {
                'status_id': self.status.id,
                'status_name': self.status.name
            }
        else:
            return None
    def get_product_info(self):
        if self.product:
            return {
                'batch_id': self.product.batch_id,
                'name': self.product.name
            }
        else:
            return None
        

class Order(models.Model):
    trans_id = models.CharField(primary_key=True, max_length=70)
    shipment_id = models.CharField(max_length=255, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='owner')
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, db_column='product')  
    logtime = models.CharField(max_length=255)
    item_count = models.CharField(max_length=255, null=True)  
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True, db_column='status')

    class Meta:
        db_table = 'Orders'
        ordering = ['-logtime']

    def get_status_info(self):
        if self.status:
            return {
                'status_id': self.status.id,
                'status_name': self.status.name
            }
        else:
            return None
        
    def get_product_info(self):
        if self.product:
            return {
                'product_id': self.product.trans_id,
                'product_name': self.product.name,
                'product_owner': self.product.owner.id
            }
        else:
            return None
    def get_requester_info(self):
        if self.owner:
            return {
                'requester_id': self.owner.id,
                'requester_name': self.owner.name
            }
        else:
            return None
        
class ShippingRequest(models.Model):
    trans_id = models.CharField(primary_key=True, max_length=70)
    product_order = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='product_order')
    lg = models.ForeignKey(User, on_delete=models.CASCADE, db_column='lg')
    reward = models.FloatField()
    status = models.ForeignKey(ShippingStatus, on_delete=models.SET_NULL, null=True, db_column='status')
    logtime = models.CharField(max_length=255)
    item_count = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    zipcode = models.CharField(max_length=64)
    building = models.CharField(max_length=64)

    class Meta:
        db_table = 'Shipping_Requests'
        ordering = ['-logtime']

    def get_status_info(self):
        if self.status:
            return {
                'status_id': self.status.id,
                'status_name': self.status.name
            }
        else:
            return None
    
    def get_order_info(self):
        if self.product_order:
            return {
                'order_id': self.product_order.trans_id,
                'product_id': self.product_order.product.trans_id,
                'product_name': self.product_order.product.name,
                'shipment_id': self.product_order.shipment_id,
            }
        else:
            return None
        

class SystemLog(models.Model):
    trans_id = models.CharField(primary_key=True, max_length=70)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='owner')
    logtime = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = 'Log'
        ordering = ['-logtime']

    def get_owner_info(self):
        if self.owner:
            return {
                'owner_id': self.owner.id,
                'owner_name': self.owner.name
            }
        else:
            return None
        
class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    noti_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='noti_user')
    description = models.TextField()
    opened = models.IntegerField()
    logtime = models.CharField(max_length=255)

    class Meta:
        db_table = 'Notifications'
        ordering = ['-logtime']
