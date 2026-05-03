from drf_spectacular.utils import extend_schema, OpenApiExample
import random
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import OTP, User
from .serializers import SendOTPSerializer, VerifyOTPSerializer
from rest_framework_simplejwt.tokens import RefreshToken
#___________________________________________________________________________________________
class SendOTPView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Users / OTP"],
        summary="Send OTP to phone number",
        description="Send a one-time password (OTP) to the given phone number.",
        request=SendOTPSerializer,
        examples=[
            OpenApiExample(
                "Send OTP Example",
                value={"phone_number": "09123456789"},
                request_only=True,
            ),
        ],
        responses={
            200: OpenApiExample(
                "OTP Sent",
                value={"detail": "OTP sent successfully"},
            ),
            400: OpenApiExample(
                "Validation Error",
                value={"phone_number": ["This field is required."]},
            ),
        },
    )
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data["phone_number"]
        code = str(random.randint(100000, 999999))

        # منقضی کردن OTPهای قبلی
        OTP.objects.filter(phone_number=phone, is_used=False).update(is_used=True)

        OTP.objects.create(
            phone_number=phone,
            code=code
        )

        # فعلاً شبیه‌سازی ارسال SMS
        print("OTP:", code)

        return Response(
{"detail": "OTP sent successfully"},
            status=status.HTTP_200_OK
        )
#___________________________________________________________________________________________
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Users / OTP"],
        summary="Verify OTP and login/register user",
        description=(
            "This endpoint verifies the OTP code sent to the user's phone number. "
            "If the user does not exist, it will be created automatically. "
            "On success, JWT tokens are returned."
        ),
        request=VerifyOTPSerializer,
        examples=[
            OpenApiExample(
                "Verify OTP Example",
                value={
                    "phone_number": "09123456789",
                    "code": "123456"
                },
                request_only=True,
            ),
        ],
        responses={
            200: OpenApiExample(
                "JWT Tokens",
                value={
                    "refresh": "jwt_refresh_token_here",
                    "access": "jwt_access_token_here"
                },
            ),
            400: OpenApiExample(
                "Invalid or Expired OTP",
                value={"error": "OTP is invalid or expired"},
            ),
        },
    )
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

        if not otp or otp.is_expired():
            return Response(
                {"error": "OTP is invalid or expired"},
                status=status.HTTP_400_BAD_REQUEST
            )

        otp.is_used = True
        otp.save()

        user, created = User.objects.get_or_create(phone_number=phone)
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK
        )
