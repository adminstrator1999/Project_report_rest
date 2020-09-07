from django.urls import path
from order.views import OrderItem, GetOrder

app_name = 'order'
urlpatterns = [
    path('order-item-list/', OrderItem.as_view(), name='order-item'),
    path('completed-order/', GetOrder.as_view(), name="completed-order")
]

