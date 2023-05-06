from django.db import models
from softdel.models import SoftDeleteModel


class Role(SoftDeleteModel):
    class Meta:
        db_table = 'role'


class User(SoftDeleteModel):
    class Meta:
        db_table = 'user'

    role = models.ForeignKey('Role', on_delete=models.CASCADE)
