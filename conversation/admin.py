from django.contrib import admin

from .models import conversation, conversationMessage

admin.site.register(conversation)
admin.site.register(conversationMessage)

