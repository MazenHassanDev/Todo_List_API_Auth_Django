from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')

    class Meta:
        db_table = 'todos'

    def __str__ (self):
        return self.title