from django.db import models


class SexChoices(models.TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'

class RoleChoices(models.IntegerChoices):
    OWNER = 5
    MANAGER = 4
    ASST_MANAGER = 3
    TEAM_LEADER = 2
    WORKER = 1
    NONE = 0
