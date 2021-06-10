from django.db import models
from django.conf import settings

# Create your models here.


class VisibilityAttribute(models.Model):
    visibility = models.CharField(max_length=10)


class Projects(models.Model):
    name = models.CharField(max_length=50)
    descriptions = models.TextField(max_length=1000)
    visibility = models.ForeignKey(VisibilityAttribute, on_delete=models.PROTECT, default="1")
    status = models.CharField(max_length=10)
    deadline = models.DateField(max_length=10)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ProjectMembers(models.Model):
    project_id = models.ForeignKey(Projects, on_delete=models.PROTECT)
    member_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    member_status = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)