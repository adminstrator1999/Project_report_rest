from django.db import transaction
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import RegistrationSerializer


class Register(APIView):
    def post(self, request):
        with transaction.atomic():
            serialier = RegistrationSerializer(data=request.data)
            data = []
            if serialier.is_valid():
                try:
                    serialier.save()
                    data.append({"response": "Tabriklayman, siz muvafaqqiyatli royhatdan o`tdingiz"})

                except ValidationError as e:
                    data = e.args[0]
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)

            else:
                data = serialier.errors
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            return Response(data, status=status.HTTP_201_CREATED)


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'is_superuser': user.is_superuser,
            'is_logged_in': user.is_authenticated
        })


class Logout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
