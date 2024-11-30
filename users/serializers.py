
from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from users.auth import UserAuthentication



class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password',
                  'organization', 'role', 'last_activity',
                  'users_role']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
            'last_activity': {'read_only': True},
            'organization': {'write_only': True},
            'role': {'write_only': True},
            'users_role': {'read_only': True},
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=155, min_length=6)
    password=serializers.CharField(max_length=68, write_only=True)
    full_name=serializers.CharField(max_length=255, read_only=True)
    access_token=serializers.CharField(max_length=255, read_only=True)
    refresh_token=serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role', 'token']
        extra_kwargs = {
            'id': {'read_only': True},
            'role': {'read_only': True},
            'password': {'write_only': True},
            'token': {'read_only': True},
        }

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        request=self.context.get('request')
        user = authenticate(request, username=username, password=password)
        if not user:
            raise AuthenticationFailed("invalid credential try again")
       
        token = UserAuthentication.encrypt_payload(payload={"id": str(user.id)})
        return {
            'id': user.id,
            'username':user.username,
            'role': user.users_role,
            'token': token,
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',  'email', 'username', 'role']


# class PasswordResetRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField(max_length=255)

#     class Meta:
#         fields = ['email']

#     def validate(self, attrs):
#         email = attrs.get('email')
#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
#             token = PasswordResetTokenGenerator().make_token(user)
            
#             # Use the frontend URL
#             frontend_url = settings.FRONTEND_URL
#             #relative_link = reverse('reset-password-confirm', kwargs={'uidb64': uidb64, 'token': token})
#             abslink = f"{frontend_url}/reset-password/{uidb64}/{token}"
            
#             email_body = f"Hi {user.first_name}, use the link below to reset your password:\n{abslink}"
#             data = {
#                 'email_body': email_body,
#                 'email_subject': "Reset your Password",
#                 'to_email': user.email
#             }
#             self.send_mail(data)
#         return super().validate(attrs)

#     def send_mail(self, data):
#         email = EmailMessage(
#             subject=data['email_subject'],
#             body=data['email_body'],
#             to=[data['to_email']]
#         )
#         email.send()




# class SetNewPasswordSerializer(serializers.Serializer):
#     password=serializers.CharField(max_length=100, min_length=6, write_only=True)
#     confirm_password=serializers.CharField(max_length=100, min_length=6, write_only=True)
#     uidb64=serializers.CharField(min_length=1, write_only=True)
#     token=serializers.CharField(min_length=3, write_only=True)

#     class Meta:
#         fields = ['password', 'confirm_password', 'uidb64', 'token']

#     def validate(self, attrs):
#         try:
#             token=attrs.get('token')
#             uidb64=attrs.get('uidb64')
#             password=attrs.get('password')
#             confirm_password=attrs.get('confirm_password')

#             user_id=force_str(urlsafe_base64_decode(uidb64))
#             user=User.objects.get(id=user_id)
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 raise AuthenticationFailed("reset link is invalid or has expired", 401)
#             if password != confirm_password:
#                 raise AuthenticationFailed("passwords do not match")
#             user.set_password(password)
#             user.save()
#             return user
#         except Exception as e:
#             return AuthenticationFailed("link is invalid or has expired")


    
# class LogoutUserSerializer(serializers.Serializer):
#     refresh_token=serializers.CharField()

#     default_error_message = {
#         'bad_token': ('Token is expired or invalid')
#     }

#     def validate(self, attrs):
#         self.token = attrs.get('refresh_token')

#         return attrs

#     def save(self, **kwargs):
#         try:
#             token=RefreshToken(self.token)
#             token.blacklist()
#         except TokenError:
#             return self.fail('bad_token')


# class UserProfileSerializer(serializers.ModelSerializer):
#     image = serializers.ImageField(required=False)

#     class Meta:
#         model = User
#         fields = ['id', 'email', 'first_name', 'last_name',"image"]
#         read_only_fields = ['email', 'date_joined']

#     def update(self, instance, validated_data):
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.last_name = validated_data.get('last_name', instance.last_name)
    
#         #instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        
#         instance.save()

#         return instance