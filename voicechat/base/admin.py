from django.contrib import admin
from .models import Task, CustomUser, Conversation
# Register your models here.

admin.site.register(Task)
admin.site.register(CustomUser)
admin.site.register(Conversation)
