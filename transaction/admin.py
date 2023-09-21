from django.contrib import admin
from users.models import Users, Organization
from transaction.models import Lunches

# Register your models here.
admin.site.register(Users)
admin.site.register(Lunches)
admin.site.register(Organization)
