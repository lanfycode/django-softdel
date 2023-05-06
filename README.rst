django-softdel
======================
English | `简体中文  <./README-zh_CN.rst>`__\

Implemented a model for soft deletion (logical deletion)
Soft deletion:
    The deleted data in the application layer is not deleted in the database
    but is shielded from the application layer

Feature
----
Inheriting the SoftDeleteModel model will result in the following features:
-  Automatically add a field `delete_time` [field name configurable]
-  Data will be marked as deleted and will not be removed from the database on delete
-  Automatically add deleted filter rule to the current QuerySet(include relation QuerySet) [optional]
-  Tables with foreign key relationships will also undergo soft deletion during cascading deletion [optional]
-  Fields with unique constraints will be adjusted to joint unique constraints with 'delete_time' [optional]

Example
----

1. Install package::

    pip install django-softdel

2. install softdel app

   .. code:: python

       INSTALLED_APPS =[
           "softdel",
           ...
       ]

3. Inherit model

   .. code:: python

       from django.db import models
       from softdel.models import SoftDeleteModel

       class YourModel(SoftDeleteModel):
           pass


4. Migration::

    python manage.py makemigrations
    python manage.py migrate

