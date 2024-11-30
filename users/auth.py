from django.contrib.auth.backends import ModelBackend
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from django.conf import settings
from datetime import datetime, timedelta
from users.models import User


class CustomUserAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None


class UserAuthentication(BaseAuthentication):
    """handle user authentication"""

    def authenticate(self, request):
        """authenticate user"""

        token = self.extract_token(request)
        if token is None:
            return None
        
        try:
            payload = jwt.decode(token, key=settings.SECRET_KEY,
                                 algorithms=['HS256'])
            self.verify_payload(payload)
            user = User.objects.get(id=payload.get('id'))
            return (user, token)
        except ExpiredSignatureError:
            raise AuthenticationFailed('Expired Token Error')
        except InvalidTokenError:
            raise AuthenticationFailed('Invalid Token Error')
        except User.DoesNotExist:
            raise AuthenticationFailed('User Does Not Exist')
    
    def verify_payload(self, payload):
        """verify token expiration"""
        
        exp = payload.get('exp')
        if not exp:
            raise InvalidTokenError('Token has no valid Expiration')
        
        current_timestamp = datetime.now().timestamp()
        if current_timestamp > exp:
            raise ExpiredSignatureError('Token is expired')
    
    def extract_token(self, request):
        """extract token from header"""

        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        return None

    @staticmethod
    def encrypt_payload(payload):
        """encrypt users payload"""

        expiry = payload.get('exp', 24)
        exp = datetime.now() + timedelta(hours=expiry)
        payload['exp'] = exp
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY,
                           algorithm='HS256')
        return token
