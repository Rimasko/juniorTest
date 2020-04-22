from django.db import models
from django.db.models.query import QuerySet


class CustomerQuerySet(QuerySet):
    def riches(self):
        """Возвращает первые пять из списка покупателей"""
        return self.all()[:5]


class CustomerManager(models.Manager):
    def get_query_set(self):
        return CustomerQuerySet(self.model)

    def __getattr__(self, attr, *args):
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)
