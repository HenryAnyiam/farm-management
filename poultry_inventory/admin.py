from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register( FlockInventory)
admin.site.register(FlockInventoryHistory)
admin.site.register( EggInventory)
admin.site.register(EggInventoryHistory)
admin.site.register(FarmData)