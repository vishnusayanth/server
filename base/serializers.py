from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from base.models import Developer


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if not Developer.objects.filter(username=username).exists():
            get_user_model().objects.create_user(username=username, password=password)
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )
        attrs['user'] = user
        return attrs
