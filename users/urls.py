from django.urls import path, include
from rest_framework import routers
from unicodedata import name
from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView,)

from .views import *

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'', CustomUserViewSet, basename='users')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    
    path('verify-email/', VerifyUserEmail.as_view(), name='verify'),

    path('profile/', getUserProfile, name= 'users-profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginUserView.as_view(), name='login-user'),
    path('get-something/', TestingAuthenticatedReq.as_view(), name='just-for-testing'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='reset-password-confirm'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
    path('logout/', LogoutApiView.as_view(), name='logout'),
    

    path('assign-farm-owner/', AssignFarmOwnerView.as_view(), name='assign-farm-owner'),
    path('assign-farm-manager/', AssignFarmManagerView.as_view(), name='assign-farm-manager'),
    path('assign-assistant-farm-manager/', AssignAssistantFarmManagerView.as_view(), name='assign-assistant-farm-manager'),
    path('assign-team-leader/', AssignTeamLeaderView.as_view(), name='assign-team-leader'),
    path('assign-farm-worker/', AssignFarmWorkerView.as_view(), name='assign-farm-worker'),

    path('dismiss-farm-manager/', DismissFarmManagerView.as_view(), name='dismiss-farm-manager'),
    path('dismiss-assistant-farm-manager/', DismissAssistantFarmManagerView.as_view(), name='dismiss-assistant-farm-manager'),
    path('dismiss-team-leader/', DismissTeamLeaderView.as_view(), name='dismiss-team-leader'),
    path('dismiss-farm-worker/', DismissFarmWorkerView.as_view(), name='dismiss-farm-worker'),

    path('', include(router.urls))
]
