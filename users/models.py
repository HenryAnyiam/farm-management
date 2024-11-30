from django.contrib.auth.models import AbstractUser
from users.choices import *
from users.validators import *
from django.db import models
from uuid import uuid4
from django.utils import timezone
# Create your models here.

class BaseModel(models.Model):
    """Abstract model for other models"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """override default save method"""

        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['-created_at']

class Organization(BaseModel):

    name = models.CharField(max_length=250)

class User(BaseModel, AbstractUser):

    email = models.EmailField(unique=True, blank=True, null=True)
    username = models.CharField(unique=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='users', null=True)
    role = models.IntegerField(choices=RoleChoices.choices, default=RoleChoices.NONE)
    last_activity = models.TextField(default='No Activity')

    @property
    def users_role(self):
        roles = ["None", "Worker", "Team Leader", "Asst Manager", "Manager", "Owner"]
        return roles[self.role]
