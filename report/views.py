from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import Order_detail, Client, Order
from report.serializers import ReportSerializer, ClientSerializer, OrderSerializer, OrderItemSerializer
from storage.models import Storage


class Report(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date_default = datetime.today() - timedelta(days=7)
        start_date_default = start_date_default.date()
        end_date_default = datetime.today().date() + timedelta(days=1)
        orders = Order_detail.objects.filter(order__start_date__gt=start_date_default,
                                             order__start_date__lt=end_date_default,
                                             order__order_types="selling", order__company=request.user.company.id)
        products = []
        for order in orders:
            products.append(order.product)

        report_data = gathering_data(product_list=set(products), report_data=[], start_date=start_date_default,
                                     end_date=end_date_default, company=request.user.company.id)
        serializer = ReportSerializer(report_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        start_date_default = datetime.today() - timedelta(days=7)
        start_date_default = start_date_default.date()
        end_date_default = datetime.today().date() + timedelta(days=1)

        start_date = request.data['start_date']
        end_date = request.data['end_date']
        date = request.data['date']
        if start_date:
            start_date = get_date_from_string(start_date)
        else:
            start_date = start_date_default
        if end_date:
            end_date = get_date_from_string(end_date)
        else:
            end_date = end_date_default
        if date:
            date = int(date)
            start_date = datetime.today() - timedelta(days=date)
            start_date = start_date.date()

        orders = Order_detail.objects.filter(order__start_date__gt=start_date, order__start_date__lt=end_date,
                                             order__order_types="selling", order__company=request.user.company.id)
        products = []
        for order in orders:
            products.append(order.product)

        report_data = gathering_data(product_list=set(products), report_data=[], start_date=start_date,
                                     end_date=end_date,
                                     company=request.user.company.id)
        serializer = ReportSerializer(report_data, many=True)
        return Response(serializer.data)


def gathering_data(product_list, report_data, start_date, end_date, company):
    for product in product_list:
        sold_products = Order_detail.objects.filter(product=product, order__start_date__gt=start_date,
                                                    order__start_date__lt=end_date,
                                                    order__order_types="selling", order__company=company)
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
    return report_data


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
            data = {'order_id': order_id, 'order_type': order_type, 'unpaid_portion': unpaid_portion,
                    'created_date': created_date,
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


def get_date_from_string(date_str):
    format_str = '%Y-%m-%d'  # The format
    return datetime.strptime(date_str, format_str)
