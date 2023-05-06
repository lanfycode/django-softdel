from django.db.models import Q
from django.db.models.sql import Query

from .config import QUERY, FILTER_DELETED


class SoftDeleteQuery(Query):
    """Add deleted filter rule to the current QuerySet"""

    def _filter_deleted(self):
        applied = getattr(self, '_filter_deleted_applied', False)
        if applied:
            return
        self.add_q(Q(**QUERY))
        self._filter_deleted_applied = True

    def get_compiler(self, *args, **kwargs):
        if FILTER_DELETED:
            self._filter_deleted()
        return super(SoftDeleteQuery, self).get_compiler(*args, **kwargs)

    def set_limits(self, low=None, high=None):
        if FILTER_DELETED:
            self._filter_deleted()
        return super(SoftDeleteQuery, self).set_limits(low, high)
