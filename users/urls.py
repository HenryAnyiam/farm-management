from django.urls import path
from rest_framework import routers
from django.urls import path

from .views import *

app_name = 'users'

router = routers.DefaultRouter()

urlpatterns = [
    path('login/', auth_user, name='login-user'),
    path('profile/', getUserProfile, name= 'users-profile'),
    path('staff/', StaffView.as_view(), name='staffs')



    # path('register/', RegisterView.as_view(), name='register'),
    # path('verify-email/', VerifyUserEmail.as_view(), name='verify'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # path('get-something/', TestingAuthenticatedReq.as_view(), name='just-for-testing'),
    # path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    # path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='reset-password-confirm'),
    # path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
    # path('logout/', LogoutApiView.as_view(), name='logout'),
    

    # path('assign-farm-owner/', AssignFarmOwnerView.as_view(), name='assign-farm-owner'),
    # path('assign-farm-manager/', AssignFarmManagerView.as_view(), name='assign-farm-manager'),
    # path('assign-assistant-farm-manager/', AssignAssistantFarmManagerView.as_view(), name='assign-assistant-farm-manager'),
    # path('assign-team-leader/', AssignTeamLeaderView.as_view(), name='assign-team-leader'),
    # path('assign-farm-worker/', AssignFarmWorkerView.as_view(), name='assign-farm-worker'),

    # path('dismiss-farm-manager/', DismissFarmManagerView.as_view(), name='dismiss-farm-manager'),
    # path('dismiss-assistant-farm-manager/', DismissAssistantFarmManagerView.as_view(), name='dismiss-assistant-farm-manager'),
    # path('dismiss-team-leader/', DismissTeamLeaderView.as_view(), name='dismiss-team-leader'),
    # path('dismiss-farm-worker/', DismissFarmWorkerView.as_view(), name='dismiss-farm-worker'),
]
