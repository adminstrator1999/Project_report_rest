from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import Order_detail, Client, Order
from product.models import Product
from report.serializers import ReportSerializer, ClientSerializer, OrderSerializer, OrderItemSerializer
from storage.models import Storage


class Report(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        report_data = []
        for product in products:
            sold_products = Order_detail.objects.filter(product=product, order__order_types='selling')
            sold_quantity = 0
            income = 0
            for sold_product in sold_products:
                sold_quantity += sold_product.quantity
                income += sold_product.price * sold_product.quantity
            item = Storage.objects.get(product=product)
            if item.rest != 0:
                expenditure_per_product = item.total_price / item.rest
                expenditure = sold_quantity * expenditure_per_product
            else:
                expenditure = 0
            report_data.append({
                'product_name': product.name,
                'sold_quantity': sold_quantity,
                'income': income,
                'expenditure': expenditure
            })
        serializer = ReportSerializer(report_data, many=True)
        return Response(serializer.data)


class History(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clients = Client.objects.all()
        serializer_objects = []
        for client in clients:
            orders = Order.objects.filter(client=client)
            name = client.name
            id = client.id
            type = client.type
            unpaid_portion = 0
            for order in orders:
                unpaid_portion += order.unpaid_portion
            data = {'name': name, 'client_id': id, 'unpaid_portion': unpaid_portion, 'type': type}
            serializer_objects.append(data)
        serializer = ClientSerializer(serializer_objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        client_id = request.data['client_id']
        orders = Order.objects.filter(client_id=client_id)
        serializer_objects = []
        for order in orders:
            order_id = order.id
            order_type = order.order_types
            unpaid_portion = order.unpaid_portion
            created_date = order.start_date
            deadline = order.deadline
            data = {'order_id': order_id, 'order_type': order_type, 'unpaid_portion': unpaid_portion, 'created_date': created_date,
                    'deadline': deadline}
            serializer_objects.append(data)
        serializer = OrderSerializer(serializer_objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        order_id = request.data['client_order_id']
        order = Order.objects.get(id=order_id)
        paid_portion = request.data['paid_portion']
        order.unpaid_portion -= int(paid_portion)
        order.save()
        return Response(status=status.HTTP_200_OK)


class ClientOrderItem(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        client_order_id = request.data['client_order_id']
        orderItems = Order_detail.objects.filter(order_id=client_order_id)
        serializer_objects = []
        for orderItem in orderItems:
            product_name = orderItem.product.name
            quantity = orderItem.quantity
            price = orderItem.price
            data = {'product_name': product_name, 'quantity': quantity, 'price': price}
            serializer_objects.append(data)
        serializer = OrderItemSerializer(serializer_objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
