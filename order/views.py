from datetime import datetime

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from order.models import Client
from order.serializers import OrderSerializer, OrderDetailSerializer, OrderItemSerializer
from product.models import Product
from storage.models import Storage


class OrderItem(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        company = request.user.company.id
        OrderItems = []
        products = Product.objects.filter(company=company)
        for product in products:
            product_id = product.id
            product_name = product.name
            last_price = Storage.objects.get(product=product).last_price
            rest = Storage.objects.get(product=product).rest
            OrderItem = {
                'product_id': product_id,
                'product_name': product_name,
                'last_price': last_price,
                'rest': rest
            }
            OrderItems.append(OrderItem)
        serializer = OrderItemSerializer(OrderItems, many=True)
        return Response(serializer.data)


class GetOrder(APIView):
    def post(self, request):
        company = request.user.company.id
        with transaction.atomic():
            orderItems = request.data["orderItems"]
            # updating storage
            try:
                update_storage(orderItems)
            except BaseException as e:
                return Response({'storage_error': e.args}, status=status.HTTP_400_BAD_REQUEST)
            # gathering data
            client_name = request.data["client"]
            payed_portion = request.data["payed_portion"]
            deadline = request.data['deadline']
            buying = orderItems[0]['buying']
            if not deadline:
                deadline = datetime.today().date()
            else:
                deadline = get_date_from_string(deadline).date()
            payed_portion = int(payed_portion)
            total_price = 0
            for item in orderItems:
                total_price += int(item['quantity']) * int(item['price'])
            unpaid_portion = total_price - payed_portion
            if client_name:
                try:
                    if buying:
                        client = Client.objects.get(name=client_name, company_id=company, type='selling')
                    else:
                        client = Client.objects.get(name=client_name, company_id=company, type='buying')
                except Client.DoesNotExist:
                    if buying:
                        client = Client.objects.create(name=client_name, company_id=company, type='selling')
                    else:
                        client = Client.objects.create(name=client_name, company_id=company, type='buying')
                if buying:
                    data = {'order_types': 'buying', 'deadline': deadline, 'client': client.id,
                            'unpaid_portion': unpaid_portion, 'company': company}
                else:
                    data = {'order_types': 'selling', 'deadline': deadline, 'client': client.id,
                            'unpaid_portion': unpaid_portion, 'company': company}
            else:
                if buying:
                    data = {'order_types': 'buying', 'deadline': deadline, 'client': '',
                            'unpaid_portion': unpaid_portion, 'company': company}
                else:
                    data = {'order_types': 'selling', 'deadline': deadline, 'client': '',
                            'unpaid_portion': unpaid_portion, 'company': company}
            # creating order
            serializer = OrderSerializer(data=data)
            if serializer.is_valid():
                order = serializer.save()
            # creating orderItems with order id
            order_serializer_items = []
            order_id = order.id
            for orderItem in orderItems:
                data = {'product': orderItem["product_id"], 'order': order_id, 'price': orderItem["price"],
                        'quantity': orderItem["quantity"]}
                order_serializer_items.append(data)
            serializer = OrderDetailSerializer(data=order_serializer_items, many=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


def get_date_from_string(date_str):
    format_str = '%Y-%m-%d'  # The format
    return datetime.strptime(date_str, format_str)


def update_storage(items):
    for item in items:
        storage_error = []
        product_id = item['product_id']
        price = int(item['price'])
        quantity = int(item['quantity'])
        product_storage = Storage.objects.get(product_id=product_id)
        if item['buying']:
            product_storage.rest += quantity
            product_storage.total_price += quantity * price
            product_storage.last_price = price
            product_storage.market_price = price
            product_storage.save()
        else:
            if product_storage.rest >= quantity:
                product_storage.total_price -= (product_storage.total_price / product_storage.rest) * quantity
                product_storage.rest -= quantity
                product_storage.save()
            else:
                storage_error.append(f"{product_storage.product.name} mahsulotiga omborda yetarli zaxira mavjud emas")
                raise BaseException(storage_error)
