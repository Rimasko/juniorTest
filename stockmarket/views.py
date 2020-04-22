from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Customer, Deal
from .serializers import CustomerSerializer, DealsFileSerializer
from .utils import load_deals_file_to_db


class DealsAPIView(views.APIView):
    """
    Deal API
    GET вернет список покупателей потративших больше всех денег
    POST загружает новые сделки в формате csv
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.riches()
    permission_classes = (AllowAny,)

    @method_decorator(cache_page(60 * 3))
    def get(self, request, *args, **kwargs):
        data = {
            "response": self.serializer_class(self.queryset.all(), many=True).data
        }
        return Response(data, status=200)

    def post(self, request):
        deals_file = DealsFileSerializer(data=request.data)
        if deals_file.is_valid():
            data = load_deals_file_to_db(deals_file.validated_data['deals'])
            cache.clear()  # очищает кеш полнолстью
            return Response(data, status=200)
        else:
            data = {"Status": "Error",
                    "Desc": deals_file.errors}
            return Response(data=data, status=400)
