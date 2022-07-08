from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

class Task(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=32, null=False)
    description = models.CharField(max_length=128, null=True)
    done = models.BooleanField(default=False)

    class Meta:
        db_table = 'tasks'

class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=32)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'{self.email}'

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                  on_delete=models.CASCADE, related_name='profile')
