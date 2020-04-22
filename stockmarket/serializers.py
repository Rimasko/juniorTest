from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """
    Customer serializer class
    для сериализации вывода списка покупателей
    """
    gems = serializers.StringRelatedField(source="get_gems", many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ('username', 'spent_money', 'gems')


class DealsFileSerializer(serializers.Serializer):
    deals = serializers.FileField(allow_empty_file=False)
