from django.db import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class User(models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField(blank=True)
    nickname = models.CharField(max_length=32, blank=True)
    about_you = models.TextField(blank=True)
