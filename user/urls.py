from django.urls import path
from user.views import Register, Logout, Login
from rest_framework.authtoken import views

app_name = 'user'
urlpatterns = [
    path('register/', Register.as_view(), name="register"),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout')
]
