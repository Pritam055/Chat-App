from django.contrib import admin

from .models import Group, Chat
# Register your models here.

class ChatAdminModel(admin.ModelAdmin):
    model = Chat 
    list_display = ('user', 'group')

admin.site.register(Group)
admin.site.register(Chat, ChatAdminModel)
