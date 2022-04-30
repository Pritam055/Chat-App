from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser
from accounts.forms import UserCreationForm

# Register your models here.

# class CustomUserAdmin(admin.UserAdmi

admin.site.register( CustomUser,  UserAdmin)
