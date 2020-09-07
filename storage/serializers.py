from rest_framework import serializers


class StorageSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=123)
    rest = serializers.IntegerField()
    last_price = serializers.IntegerField()
    market_price = serializers.IntegerField()
    total_price = serializers.IntegerField()

