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

    class Meta:
        db_table = 'Materials'
        ordering = ['-logtime']