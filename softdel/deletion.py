from collections import Counter
from operator import attrgetter
from django.db import transaction
from django.db.models import sql, signals
from django.db.models.deletion import Collector

from .config import QUERY, ACTION


class SoftDeleteCollector(Collector):

    def delete(self):
        # sort instance collections
        for model, instances in self.data.items():
            self.data[model] = sorted(instances, key=attrgetter("pk"))

        # if possible, bring the models in an order suitable for databases that
        # don't support transactions or cannot defer constraint checks until the
        # end of a transaction.
        self.sort()
        # number of objects deleted for each model label
        deleted_counter = Counter()

        with transaction.atomic(using=self.using, savepoint=False):
            # send pre_delete signals
            for model, obj in self.instances_with_model():
                if not model._meta.auto_created:
                    signals.pre_delete.send(
                        sender=model, instance=obj, using=self.using
                    )

            #################
            # MODIFIED HERE #
            #################
            # for qs in self.fast_deletes:
            #     count = qs._raw_delete(using=self.using)
            #     if count:
            #         deleted_counter[qs.model._meta.label] += count
            for qs in self.fast_deletes:
                qs = qs.filter(**QUERY)
                count = qs.count()
                qs.update(**ACTION)
                deleted_counter[qs.model._meta.label] += count

            # update fields [SET, SET_NULL, SET_DEFAULT]
            for model, instances_for_fieldvalues in self.field_updates.items():
                for (field, value), instances in instances_for_fieldvalues.items():
                    query = sql.UpdateQuery(model)
                    query.update_batch([obj.pk for obj in instances],
                                       {field.name: value}, self.using)
            # reverse instance collections
            for instances in self.data.values():
                instances.reverse()

            # delete instances
            for model, instances in self.data.items():
                #################
                # MODIFIED HERE #
                #################
                # query = sql.DeleteQuery(model)
                # pk_list = [obj.pk for obj in instances]
                # count = query.delete_batch(pk_list, self.using)
                query = sql.UpdateQuery(model)
                pk_list = [obj.pk for obj in instances]
                query.update_batch(pk_list, ACTION, self.using)
                count = len(pk_list)
                if count:
                    deleted_counter[model._meta.label] += count

                if not model._meta.auto_created:
                    for obj in instances:
                        signals.post_delete.send(
                            sender=model, instance=obj, using=self.using
                        )

        return sum(deleted_counter.values()), dict(deleted_counter)
