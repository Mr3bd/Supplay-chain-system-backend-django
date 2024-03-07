from django.db import models

class User(models.Model):
    id = models.CharField(primary_key=True, max_length=64, db_index=True)
    name = models.CharField(max_length=255)
    role = models.IntegerField()
    deleted = models.IntegerField()
    class Meta:
        db_table = 'Users'