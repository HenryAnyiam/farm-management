from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField

from users.choices import *
from users.validators import *
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

from .managers import UserManager
# Create your models here.

AUTH_PROVIDERS ={'email':'email', 'google':'google', 'github':'github', 'linkedin':'linkedin'}


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True, editable=False) 
    email = models.EmailField(
        max_length=255, verbose_name=_("Email Address"), unique=True
    )
    auth_provider=models.CharField(max_length=50, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))
    registration_time = models.DateTimeField(auto_now_add=True)
    #username = models.CharField(max_length=45, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = PhoneNumberField(blank=True)
    sex = models.CharField(choices=SexChoices.choices, max_length=6)
    is_farm_owner = models.BooleanField(default=False)
    is_farm_manager = models.BooleanField(default=False)
    is_assistant_farm_manager = models.BooleanField(default=False)
    is_team_leader = models.BooleanField(default=False)
    is_farm_worker = models.BooleanField(default=False)
    is_staff =models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)


    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number' ]#'sex'

    def assign_farm_owner(self):
        self.is_farm_owner = True
        self.is_farm_manager = False
        self.is_assistant_farm_manager = False
        self.is_team_leader = False
        self.is_farm_worker = False
        self.save()

    def assign_farm_manager(self):
        self.is_farm_owner = False
        self.is_farm_manager = True
        self.is_assistant_farm_manager = False
        self.is_team_leader = False
        self.is_farm_worker = False
        self.save()

    def assign_assistant_farm_manager(self):
        self.is_farm_owner = False
        self.is_farm_manager = False
        self.is_assistant_farm_manager = True
        self.is_team_leader = False
        self.is_farm_worker = False
        self.save()

    def assign_team_leader(self):
        self.is_farm_owner = False
        self.is_farm_manager = False
        self.is_assistant_farm_manager = False
        self.is_team_leader = True
        self.is_farm_worker = True
        self.save()

    def assign_farm_worker(self):
        self.is_farm_owner = False
        self.is_farm_manager = False
        self.is_asst_farm_manager = False
        self.is_team_leader = False
        self.is_farm_worker = True
        self.save()

    def dismiss_farm_owner(self):
        self.is_farm_owner = False
        self.save()

    def dismiss_farm_manager(self):
        self.is_farm_manager = False
        self.save()

    def dismiss_assistant_farm_manager(self):
        self.is_assistant_farm_manager = False
        self.save()

    def dismiss_team_leader(self):
        self.is_team_leader = False
        self.save()

    def dismiss_farm_worker(self):
        self.is_farm_worker = False
        self.save()

    def get_full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}"

    def get_role(self):
        """Return the role of the user."""
        if self.is_farm_owner:
            return "Farm Owner"
        elif self.is_farm_manager:
            return "Farm Manager"
        elif self.is_assistant_farm_manager:
            return "Assistant Farm Manager"
        elif self.is_team_leader:
            return "Team Leader"
        elif self.is_farm_worker:
            return "Farm Worker"
        else:
            return "Regular User"

    def get_farm_workers(self):
        return CustomUser.objects.filter(is_farm_worker=True)

    def get_team_leaders(self):
        return CustomUser.objects.filter(is_team_leader=True)

    def get_assistant_farm_managers(self):
        return CustomUser.objects.filter(is_assistant_farm_manager=True)

    def get_farm_managers(self):
        return CustomUser.objects.filter(is_farm_manager=True)

    def get_farm_owners(self):
        return CustomUser.objects.filter(is_farm_owner=True)

  
   


    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def tokens(self):    
        refresh = RefreshToken.for_user(self)
        return {
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }


    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"


class OneTimePassword(models.Model):
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp=models.CharField(max_length=6)


    def __str__(self):
        return f"{self.user.first_name} - otp code"
    



class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} - {self.login_time}"
    




class UserRegistration(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    registration_time = models.DateTimeField(auto_now_add=True)