from django.urls import path
from .views import SendOTPView, VerifyOTPView
from rest_framework_simplejwt.views import TokenObtainPairView
urlpatterns = [
    path('send-otp/', SendOTPView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
