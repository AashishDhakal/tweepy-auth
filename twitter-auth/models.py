from django.db import models

# Create your models here.


class User(models.Model):
    access_token = models.TextField(unique=True)
    access_secret = models.TextField()
