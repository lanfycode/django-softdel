from django.db import models
from django.db import router
from django.db.models.manager import Manager

from .deletion import SoftDeleteCollector
from .manager import SoftDeleteManager
from .config import FIELD_NAME, COLLECT_RELATED


class SoftDeleteModel(models.Model):
    """
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

    实现了软删(逻辑删除)的模型
    软删的概念：应用层已删除的数据在数据库中并没有被删除，而是对应用层屏蔽

    特性
    ----
    继承SoftDeleteModel的model会获得以下特性：

    -  自动增加一个字段`delete_time`【字段名可配置】
    -  执行删除操作时数据会被标记为'已删除'，并不会从数据库移除
    -  自动过滤已删除数据的规则（包括关联查询） 【是否自动过滤可配置】
    -  有外键关系的表在级联删除时也会进行软删 【是否管理级联可配置】
    -  有唯一约束的字段会被调整为与`delete_time`的联合唯一约束 【是否修改约束可配置】
    """
    objects = SoftDeleteManager()
    base_objects = Manager()  # django Manager

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft delete"""
        using = using or router.db_for_write(self.__class__, instance=self)
        assert self.pk is not None, (
                "%s object can't be deleted because its %s attribute is set to None." %
                (self._meta.object_name, self._meta.pk.attname)
        )
        #################
        # MODIFIED HERE #
        #################
        collector = SoftDeleteCollector(using=using)
        collector.collect([self], keep_parents=keep_parents, collect_related=COLLECT_RELATED)
        return collector.delete()


SoftDeleteModel.add_to_class(FIELD_NAME, models.FloatField(default=0, editable=False))
