from django.urls import path
from .views import SendOTPView, VerifyOTPView
from rest_framework_simplejwt.views import TokenRefreshView
#___________________________________________________________________________________________
urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
