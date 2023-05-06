django-softdel
======================
`English <./README.rst>`__ \| 简体中文

提供一个实现了软删(逻辑删除)的模型： SoftDeleteModel

软删的概念：应用层已删除的数据在数据库中并没有被删除，而是对应用层屏蔽


特性
----
继承SoftDeleteModel的model会获得以下特性

-  会自动增加一个字段delete_time【字段名可配置】
-  执行删除操作时将更新字段delete_time标记为'已删除'，而不会真实删除数据库中的数据
-  执行查询（包括关联查询和反向关联查询）操作时将自动过滤'已删除'的数据 【是否自动过滤可配置】
-  有外键关系的表在级联删除时也会进行软删 【是否管理级联可配置】
-  为字段设置unique=True时，将会被改为和delete_time的联合唯一约束 【是否修改约束可配置】

例子
----

1. 下载python包::

    pip install django-softdel

2. 添加 softdel app

   .. code:: python

       INSTALLED_APPS =[
           "softdel",
           ...
       ]

3. 继承 model

   .. code:: python

       from django.db import models
       from softdel.models import SoftDeleteModel

       class YourModel(SoftDeleteModel):
           pass


4. 执行数据库迁移::

    python manage.py makemigrations
    python manage.py migrate

