from django.contrib import admin
from .models import Lunches
from users.models import Organization
# Register your models here.
admin.site.register(Lunches)
admin.site.register(Organization)