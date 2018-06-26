from django.contrib import admin

from .models.user import User
from .models.race import Race
from .models.horse import  Horse


# Register your models here.

admin.site.register(User)
admin.site.register(Race)
admin.site.register(Horse)

