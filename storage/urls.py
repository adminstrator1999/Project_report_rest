from django.urls import path
from storage.views import StorageList

app_name = 'storage'
urlpatterns = [
    path('', StorageList.as_view(), name="storage")
]
