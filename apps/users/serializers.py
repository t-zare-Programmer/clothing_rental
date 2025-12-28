from rest_framework import serializers
from .models import User
#___________________________________________________________________________________________
class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
#___________________________________________________________________________________________
class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=6)
#___________________________________________________________________________________________
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number')
