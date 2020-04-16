from django.db import models


class Customer(models.Model):
    """
    модель покупателя
    """
    username = models.CharField("Логин", max_length=30)
    spent_money = models.IntegerField("потрачено за весь период", default=0)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["-spent_money"]

    def get_gems(self):
        rich_set = Customer.objects.all()[:5]
        current_gems = self.deals.values('item').distinct()
        gems_list = [gem["item"] for gem in current_gems]
        gems = []
        for rich in rich_set:
            if rich.id != self.id:
                intersection = Deal.objects.filter(item__in=gems_list, customer=rich).values('item').distinct()
                gems +=([gem["item"] for gem in intersection])
        return gems


class Deal(models.Model):
    """
    модель сделки
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Клиент", related_name="deals")
    item = models.CharField("Наименование товара", max_length=30)
    total = models.PositiveIntegerField("Сумма сделки")
    quantity = models.PositiveSmallIntegerField("количество товара, шт.")
    date = models.DateTimeField("дата и время регистрации сделки")

    class Meta:
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"
