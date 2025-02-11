from django.urls import path, include
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import RegisterUser, CustomAuthToken , RequestPasswordResetOTPView, VerifyPasswordResetOTPView

router = DefaultRouter()
router.register(r'users', RegisterUser, basename='user')


urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='Login'),
    path('', include(router.urls)),
    path("request-password-reset-otp/", RequestPasswordResetOTPView.as_view(), name="request_password_reset_otp"),
    path("verify-password-reset-otp/", VerifyPasswordResetOTPView.as_view(), name="verify_password_reset_otp"),
]

'''
 Request Password Reset OTP

Endpoint:
POST /account/request-password-reset-otp/

Description:
Sends a one-time password (OTP) to the user's registered email for password reset.

Request Body:
{
  "email": "user@example.com"
}
Response (Success - 200 OK):
{
  "message": "OTP sent successfully."
}
Response (Error - 400 Bad Request):
{
  "error": "Invalid email or user not found."
}
'''

'''
 Reset Password with OTP

Endpoint:
POST /account/reset-password/

Description:
Verifies the OTP and allows the user to reset their password.

Request Body:
{
  "email": "user@example.com",
  "otp": "123456",
  "new_password": "NewSecurePassword123"
}

Response (Success - 200 OK):
{
  "message": "Password reset successfully."
}

Response (Error - 400 Bad Request):
{
  "error": "Invalid OTP or OTP expired."
}

'''