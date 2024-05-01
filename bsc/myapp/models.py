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