from django.contrib import admin
from users.models import Users, Organization
from transaction.models import Lunch

# Register your models here.
#admin.site.register(Users)
admin.site.register(Lunch)
#admin.site.register(Organization)
