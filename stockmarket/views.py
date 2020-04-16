import csv
import io
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Customer, Deal
from .serializers import CustomerSerializer


class DealsAPIView(mixins.ListModelMixin,
                   generics.GenericAPIView):
    """
    Deal API
    GET вернет список покупателей потративших больше всех денег
    POST загружает новые сделки в формате csv
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()[:5]
    permission_classes = (AllowAny,)

    @method_decorator(cache_page(60 * 3))
    def get(self, request, *args, **kwargs):
        data = {
            "response": self.serializer_class(self.get_queryset(), many=True).data
        }
        return Response(data, status=200)

    def post(self, request):
        if "deals" not in request.data:
            data = {"Status": "Error",
                    "Desc": "File does not exist"}
            return Response(data, status=403)
        deals = request.data.get('deals')
        if type(deals) is not InMemoryUploadedFile:
            data = {"Status": "Error",
                    "Desc": "deals must be a file"}
            return Response(data, status=403)
        if not deals.name.endswith(".csv"):
            data = {"Status": "Error",
                    "Desc": "deals must be a csv file"}
            return Response(data, status=403)
        data = self.load_deal(deals)
        cache.clear() # очищает кеш полнолстью
        return Response(data, status=200)

    @staticmethod
    def load_deal(file):
        """
        парсит csv файл и загружает в БД
        :param file: InMemoryUploadedFile
        :return: статус парсинга
        """
        deals_reader = csv.DictReader(io.StringIO(file.read().decode('utf-8')))
        for deal_row in deals_reader:
            customer, customer_created = Customer.objects.get_or_create(username=deal_row["customer"])
            deal_date = datetime.strptime(deal_row["date"], "%Y-%m-%d %H:%M:%S.%f")
            deal, created = Deal.objects.get_or_create(
                customer=customer,
                item=deal_row["item"],
                total=int(deal_row["total"]),
                quantity=int(deal_row["quantity"]),
                date=deal_date)
            if created:
                customer.spent_money += int(deal_row["total"])
                deal.save()
                customer.save()

        data = {"Status": "Ok"}
        return data
