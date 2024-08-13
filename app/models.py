from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import Group, Permission

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Poll(models.Model):
    title = models.CharField(max_length=500)
    creater = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField('Question')
    is_open = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
    
class Question(models.Model):
    title = models.CharField(max_length=500, unique=True)
    choices = models.TextField(help_text="Enter Choices By using comma to separte")

    def __str__(self) -> str:
        return self.title
    
class PollResponse(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="responses")
    user_email = models.EmailField()

    def __str__(self):
        return f"{self.user_email} - {self.poll.title}"

class PollAnswer(models.Model):
    response = models.ForeignKey(PollResponse, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.response.user_email} - {self.question.title} - {self.answer}"