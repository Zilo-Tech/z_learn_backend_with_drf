from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from authentication.api.serializers import RequestOTPSerializer, VerifyOTPSerializer


class RequestPasswordResetOTPView(generics.GenericAPIView):
    serializer_class = RequestOTPSerializer

    def post(self, request, *args, **kwargs):
        """Sends OTP to the user's email."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "OTP has been sent to your email."}, status=status.HTTP_200_OK
        )


class VerifyPasswordResetOTPView(generics.GenericAPIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request, *args, **kwargs):
        """Verifies OTP and resets the password."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Your password has been successfully reset."}, status=status.HTTP_200_OK
        )
