from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from storage.models import Storage
from storage.serializers import StorageSerializer


class StorageList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        storage_objects = Storage.objects.all()
        products = []
        for item in storage_objects:
            product_name = item.product.name
            rest = item.rest
            last_price = item.last_price
            market_price = item.market_price
            total_price = item.total_price
            data = {'product_name': product_name, 'rest': rest, 'last_price': last_price, 'market_price': market_price,
                    'total_price': total_price}
            products.append(data)
        serializer = StorageSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
