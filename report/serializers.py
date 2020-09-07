from rest_framework import serializers


class ReportSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=123)
    sold_quantity = serializers.IntegerField()
    income = serializers.IntegerField()
    expenditure = serializers.IntegerField()


class ClientSerializer(serializers.Serializer):
    client_id = serializers.IntegerField()
    name = serializers.CharField(max_length=123)
    unpaid_portion = serializers.IntegerField()
    type = serializers.CharField(max_length=123)


class OrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    order_type = serializers.CharField(max_length=123)
    unpaid_portion = serializers.IntegerField()
    created_date = serializers.DateTimeField()
    deadline = serializers.DateField()


class OrderItemSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=123)
    price = serializers.IntegerField()
    quantity = serializers.IntegerField()
