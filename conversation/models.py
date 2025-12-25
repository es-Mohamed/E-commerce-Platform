from django.contrib.auth.models import User

from django.db import models

from items.models import Item

class conversation(models.Model):
    items = models.ForeignKey(Item, related_name='conversations', on_delete=models.CASCADE, null=True, blank=True)
    members = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('modified_at',)

class conversationMessage(models.Model):
    conversation = models.ForeignKey(conversation, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="created_messages", on_delete=models.CASCADE)