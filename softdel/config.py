from time import time

from django.conf import settings
from django.utils.functional import lazy

# soft delete field name
# 已删除标记字段
FIELD_NAME = getattr(settings, 'SOFT_DELETE_FIELD_NAME', 'delete_time')

# If True, automatically add deleted filter rule to the current QuerySet(include relation QuerySet)
# 是否自动过滤已删除数据的规则（包括关联查询）
FILTER_DELETED = getattr(settings, 'SOFT_DELETE_FILTER_DELETED', True)

# If True, tables with foreign key relationships will also undergo soft deletion during cascading deletion
# 有外键关系的表在级联删除时是否进行软删
COLLECT_RELATED = getattr(settings, 'SOFT_DELETE_COLLECT_RELATED', True)

# If True, Fields with unique constraints will be adjusted to joint unique constraints with 'delete_time'
# 有唯一约束的字段是否调整为与`delete_time`的联合唯一约束
ADJUST_UNIQUE = getattr(settings, 'SOFT_DELETE_ADJUST_UNIQUE', True)

QUERY = {FIELD_NAME: 0}
ACTION = {FIELD_NAME: lazy(time)()}
