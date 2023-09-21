from django.contrib import admin

# Register your models here.
from .models import Organization, Users

admin.site.register(Organization)
admin.site.register(Users)