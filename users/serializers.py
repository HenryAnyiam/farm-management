from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
import json
from dataclasses import field
from .models import *
from rest_framework import serializers
from string import ascii_lowercase, ascii_uppercase
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.urls import reverse
from .utils import send_mail
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from .models import CustomUser


CustomUser = get_user_model()

''''
class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Custom serializer for creating user instances with additional fields.

    Fields:
    - `phone_number`: A PhoneNumberField representing the user's phone number.
                      It is a unique field that stores phone numbers in a standardized format.
                      The phone number is validated by the Django phone number package.

    Meta:
    - `model`: The User model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation when creating a user instance.
                It includes the standard UserCreateSerializer fields along with 'phone_number'
                and additional fields representing the user's roles.

    Usage:
        Use this serializer when creating a new user instance and passing the phone number field.
        The 'phone_number' field should be in a valid phone number format, for example: '+1234567890'.
        For example:
        ```
        {
            "username": "example_user",
            "password": "password123",
            "first_name": "Peter",
            "last_name": "Evance",
            "phone_number": "+1234567890",
            "sex": "Male",
            "is_farm_owner": True,
            "is_farm_manager": False,
            "is_assistant_farm_manager": False,
            "is_team_leader": False,
            "is_farm_worker": False
        }
        ```

    """
    phone_number = PhoneNumberField()

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'sex',
                  'is_farm_owner', 'is_farm_manager', 'is_assistant_farm_manager', 'is_team_leader', 'is_farm_worker')


class CustomUserSerializer(UserSerializer):
    """
    Custom serializer for retrieving and updating user instances with additional fields.

    Fields:
    - `phone_number`: A PhoneNumberField representing the user's phone number.
                      It is a unique field that stores phone numbers in a standardized format.
                      The phone number is validated by the Django phone number package.

    Meta:
    - `model`: The User model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation when retrieving or updating a user instance.
                It includes the standard UserSerializer fields along with 'phone_number'
                and additional fields representing the user's roles.

    Usage:
        Use this serializer when retrieving or updating an existing user instance.
        The 'phone_number' field can be used to retrieve or update the user's phone number.
        The 'phone_number' field should be in a valid phone number format, for example: '+1234567890'.
        For example:
        ```
        {
            "id": 1,
            "username": "example_user",
            "first_name": "Peter",
            "last_name": "Evance",
            "phone_number": "+1234567890",
            "sex": "Male",
            "is_farm_owner": True,
            "is_farm_manager": False,
            "is_assistant_farm_manager": False,
            "is_team_leader": False,
            "is_farm_worker": False
        }
        ```

    """
    phone_number = PhoneNumberField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'phone_number', 'sex', 'is_farm_owner', 'is_farm_manager'
                  , 'is_assistant_farm_manager', 'is_team_leader', 'is_farm_worker')
'''




class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'sex', 'last_name', 'password']
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            sex=validated_data.get('sex'),
            password=validated_data.get('password')
        )
        return user  # Return the actual user instance here

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=155, min_length=6)
    password=serializers.CharField(max_length=68, write_only=True)
    full_name=serializers.CharField(max_length=255, read_only=True)
    access_token=serializers.CharField(max_length=255, read_only=True)
    refresh_token=serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id','email', 'password', 'full_name', 'access_token', 'refresh_token']

    

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request=self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("invalid credential try again")
       
        tokens=user.tokens()
        return {
            'id':user.id,
            'email':user.email,
            'full_name':user.get_full_name,
            "access_token":str(tokens.get('access')),
            "refresh_token":str(tokens.get('refresh'))
        }



class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            
            # Use the frontend URL
            frontend_url = settings.FRONTEND_URL
            #relative_link = reverse('reset-password-confirm', kwargs={'uidb64': uidb64, 'token': token})
            abslink = f"{frontend_url}/reset-password/{uidb64}/{token}"
            
            email_body = f"Hi {user.first_name}, use the link below to reset your password:\n{abslink}"
            data = {
                'email_body': email_body,
                'email_subject': "Reset your Password",
                'to_email': user.email
            }
            self.send_mail(data)
        return super().validate(attrs)

    def send_mail(self, data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()




class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64=serializers.CharField(min_length=1, write_only=True)
    token=serializers.CharField(min_length=3, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            password=attrs.get('password')
            confirm_password=attrs.get('confirm_password')

            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=CustomUser.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("reset link is invalid or has expired", 401)
            if password != confirm_password:
                raise AuthenticationFailed("passwords do not match")
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            return AuthenticationFailed("link is invalid or has expired")


    
class LogoutUserSerializer(serializers.Serializer):
    refresh_token=serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')

        return attrs

    def save(self, **kwargs):
        try:
            token=RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')
        




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id',  'email', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name',"image"]
        read_only_fields = ['email', 'date_joined']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
    
        #instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        
        instance.save()

        return instance