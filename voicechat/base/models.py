from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']


class ChatMessage(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=10)  # "user" or "bot"

    def __str__(self):
        return self.content

class ChatHistory(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    messages = models.ManyToManyField(ChatMessage)

    def __str__(self):
        return f"Chat history at {self.timestamp}"

class ChatMetaData(models.Model):
    unique_id = models.CharField(max_length=20, unique=True)
    generated_name = models.CharField(max_length=10)
    date = models.DateTimeField()
    chat_history = models.ForeignKey(ChatHistory, on_delete=models.CASCADE)

    def __str__(self):
        return self.generated_name