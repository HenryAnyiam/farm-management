from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(FlockSource)
admin.site.register(FlockInspectionRecord)
admin.site.register(HousingStructure)
admin.site.register(Flock)
admin.site.register(FlockBreedInformation)
admin.site.register(FlockBreed)
admin.site.register(FlockMovement)
admin.site.register(FlockHistory)
admin.site.register(EggCollection)