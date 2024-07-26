from django.db import models
from app.models import CustomUser

# Create your models here.
class Poll(models.Model):
    title = models.CharField(max_length=500)
    creater = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    questions = models.ManyToManyField('Question')
    is_open = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
    
class Question(models.Model):
    title = models.CharField(max_length=500)
    choices = models.TextField(help_text="Enter Choices By using comma to separte")

    def __str__(self) -> str:
        return self.title