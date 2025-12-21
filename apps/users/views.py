import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from .models import OTP, User
from .serializers import SendOTPSerializer, VerifyOTPSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone_number']
        code = str(random.randint(100000, 999999))

        # OTP قبلی را (در صورت وجود) منقضی کن
        OTP.objects.filter(phone_number=phone, is_used=False).update(is_used=True)

        OTP.objects.create(
            phone_number=phone,
            code=code
        )

        # بعداً به SMS Service وصل می‌شود
        print("OTP:", code)

        return Response(
            {"message": "OTP sent successfully"},
            status=status.HTTP_200_OK
        )


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']

        otp = OTP.objects.filter(
            phone_number=phone,
            code=code,
            is_used=False
        ).last()

        if not otp:
            return Response(
                {"error": "OTP is invalid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if otp.is_expired():
            return Response(
                {"error": "OTP has expired"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # OTP مصرف شد
        otp.is_used = True
        otp.save()

        user, created = User.objects.get_or_create(phone_number=phone)

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)
