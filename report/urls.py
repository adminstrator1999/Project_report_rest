from django.urls import path
from report.views import Report, History, ClientOrderItem

app_name = 'report'
urlpatterns = [
    path('', Report.as_view(), name='report'),
    path('history/', History.as_view(), name='history'),
    path('client-order-items/', ClientOrderItem.as_view(), name='client-order-items')
]
