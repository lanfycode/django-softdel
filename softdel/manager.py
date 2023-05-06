from django.db.models.manager import Manager

from .query import SoftDeleteQuery
from .queryset import SoftDeleteQuerySet


class SoftDeleteManager(Manager):

    def get_queryset(self):
        query = SoftDeleteQuery(self.model)
        queryset = SoftDeleteQuerySet(model=self.model, query=query)
        return queryset

    def all(self):
        return self.get_queryset().all()
