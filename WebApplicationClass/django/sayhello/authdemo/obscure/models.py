from django.db import models

class MyUser(models.Model):
    id = models.IntergerField()
    username = models.CharField(max_length=16)
    email = models.EmailField(max_length = 254))
    password = models.CharField(max_legth=128)
