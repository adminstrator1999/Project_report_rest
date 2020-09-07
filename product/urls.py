from django.urls import path

from product.views import ProductList, CategoryList, CompanyList

app_name = 'product'
urlpatterns = [
    path("", ProductList.as_view(), name="product"),
    path('category/', CategoryList.as_view(), name='category'),
    path('company/', CompanyList.as_view(), name='company')
]
