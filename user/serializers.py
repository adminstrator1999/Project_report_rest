from user.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    confirmation_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'company', 'password', 'confirmation_password', 'company']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            company=self.validated_data['company'],
        )
        password = self.validated_data['password']
        confirmation_password = self.validated_data['confirmation_password']
        if password != confirmation_password:
            raise serializers.ValidationError({"password": ["Parollar mos tushishi kerak!"]})
        user.set_password(password)
        user.save()
        return user
