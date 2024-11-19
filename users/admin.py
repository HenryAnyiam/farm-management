from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(OneTimePassword)
admin.site.register( UserActivity)
admin.site.register(UserRegistration)