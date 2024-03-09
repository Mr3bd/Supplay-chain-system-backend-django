from django.db import models

class User(models.Model):
    id = models.CharField(primary_key=True, max_length=64, db_index=True)
    name = models.CharField(max_length=255)
    role = models.IntegerField()
    deleted = models.IntegerField()
    logtime = models.CharField(max_length=255)
    class Meta:
        db_table = 'Users'

class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'Roles'
        ordering = ['id']  # Order by id ascending