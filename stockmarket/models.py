from django.db import models

from stockmarket.managers import CustomerManager


class Customer(models.Model):
    """
    модель покупателя
    """
    username = models.CharField(verbose_name="Логин", max_length=30)
    spent_money = models.IntegerField(verbose_name="потрачено за весь период", default=0)
    objects = CustomerManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["-spent_money"]

    def get_gems(self):
        rich_list = Customer.objects.exclude(username=self.username)[:4]
        gems_list = set(self.deals.filter(item__in=Deal.objects.filter(customer__in=rich_list)
                                          .values_list('item', flat=True))
                        .values_list('item', flat=True))
        return set(gems_list)


class Deal(models.Model):
    """
    модель сделки
    """
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE,
                                 verbose_name="Клиент",
                                 related_name="deals")
    item = models.CharField("Наименование товара", max_length=30)
    total = models.PositiveIntegerField("Сумма сделки")
    quantity = models.PositiveSmallIntegerField("количество товара, шт.")
    date = models.DateTimeField("дата и время регистрации сделки")

    class Meta:
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"
