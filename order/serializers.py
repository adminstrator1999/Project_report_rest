from rest_framework import serializers

from order import models


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        exclude = ('start_date', )


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order_detail
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = '__all__'


class OrderItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField(max_length=123)
    last_price = serializers.IntegerField()
    rest = serializers.IntegerField()
