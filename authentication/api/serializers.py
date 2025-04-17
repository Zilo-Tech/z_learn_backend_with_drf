from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    whatsapp_number = serializers.CharField(required=True)
    email = serializers.EmailField(required=False)  # Make email optional

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'whatsapp_number']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
        
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                'error': _('The 2 passwords should match')
            })
        return data
    
    def save(self):
        password = self.validated_data['password']
        self.validated_data.pop('password2')
        username = self.validated_data['username']
        email = self.validated_data.get('email', None)  # Handle optional email
        whatsapp_number = self.validated_data['whatsapp_number']
        
        if User.objects.filter(whatsapp_number=whatsapp_number).exists():
            raise serializers.ValidationError({
                'error': _('This WhatsApp number has been taken')
            })
        
        user = User(
            username=username,
            email=email,  # Save None if email is not provided
            whatsapp_number=whatsapp_number
        )
        user.set_password(password)
        user.save()
        return user

    
class PasswordChangedSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_confirm_password = serializers.CharField(required=True,write_only=True)
    
    
    def validate_old_password(self, value):
        user = self.context['request'].user      
        if not user.check_password(value):
            raise serializers.ValidationError('Old password does not match')
        return value
    
    def validate(self, data):
        if data['new_password'] != data['new_confirm_password']:
            raise serializers.ValidationError(_('New password do not match'))
        validate_password(data['new_password'], self.context['request'].user)
        return data 
    
    def save(self, **kwargs):
        user = self.context['request'].user 
        new_password = self.validated_data['new_password']
        user.set_password(self.validated_data['new_password'])
        validate_password(new_password)
        user.save()
        return user 
    

class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """Check if email exists in the system."""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("No user found with this email address."))
        return value

    def save(self):
        """Generate OTP and send via email/SMS."""
        email = self.validated_data["email"]
        user = User.objects.get(email=email)

        # Generate a random 6-digit OTP
        otp = "".join(random.choices("0123456789", k=6))

        # Store OTP in the database
        PasswordResetOTP.objects.create(user=user, otp=otp)

        # Send OTP via email (or SMS)
        send_mail(
            subject="Your Password Reset OTP",
            message=f"Your OTP for password reset is: {otp}",
            from_email="no-reply@yourdomain.com",
            recipient_list=[email],
            fail_silently=False,
        )

        return {"message": "OTP sent to your email."}


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Check if OTP is correct and not expired."""
        email = data["email"]
        otp = data["otp"]

        # Find user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("User not found."))

        # Check OTP
        try:
            otp_entry = PasswordResetOTP.objects.filter(user=user, otp=otp, is_used=False).latest("created_at")
        except PasswordResetOTP.DoesNotExist:
            raise serializers.ValidationError(_("Invalid or expired OTP."))

        # Check OTP expiration
        if otp_entry.is_expired():
            raise serializers.ValidationError(_("OTP has expired. Request a new one."))

        # Validate passwords
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(_("Passwords do not match."))

        return data

    def save(self):
        """Reset password and mark OTP as used."""
        email = self.validated_data["email"]
        new_password = self.validated_data["new_password"]

        # Find user
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        # Mark OTP as used
        PasswordResetOTP.objects.filter(user=user).update(is_used=True)

        return {"message": "Password successfully reset."}