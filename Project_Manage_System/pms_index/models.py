from django.db import models
from django.conf import settings

# Create your models here.


class Projects(models.Model):
    name = models.CharField(max_length=50)
    deadline = models.DateField(max_length=10)
    descriptions = models.TextField(max_length=1000)
    owner = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
