from django.db.models import QuerySet

from .config import COLLECT_RELATED
from .deletion import SoftDeleteCollector


class SoftDeleteQuerySet(QuerySet):

    def delete(self):
        """Soft delete the records in the current QuerySet."""
        self._not_support_combined_queries('delete')
        assert not self.query.is_sliced, \
            "Cannot use 'limit' or 'offset' with delete."

        if self.query.distinct or self.query.distinct_fields:
            raise TypeError('Cannot call delete() after .distinct().')
        if self._fields is not None:
            raise TypeError("Cannot call delete() after .values() or .values_list()")

        queryset = self._chain()

        # The delete is actually 2 queries - one to find related objects,
        # and one to delete. Make sure that the discovery of related
        # objects is performed on the same database as the deletion.
        queryset._for_write = True

        # Disable non-supported fields.
        queryset.query.select_for_update = False
        queryset.query.select_related = False
        queryset.query.clear_ordering(force_empty=True)

        #################
        # MODIFIED HERE #
        #################
        collector = SoftDeleteCollector(using=queryset.db)
        collector.collect(queryset, collect_related=COLLECT_RELATED)
        deleted, _rows_count = collector.delete()

        # Clear the result cache, in case this QuerySet gets reused.
        self._result_cache = None
        return deleted, _rows_count
