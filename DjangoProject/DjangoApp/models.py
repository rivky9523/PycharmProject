from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


ROLE=[
    (1, "manager"),
    (2, "user"),
]
STATUS =[
    (1, "new"),
    (2, "processing")
    ,(3, "done")
]

class UserStaff(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.IntegerField(choices=ROLE, default=1)
    team = models.ForeignKey("Team",on_delete = models.CASCADE, null=True,blank=True,related_name="members")
    def __str__(self):
        return self.user.username

def end_date_validation(value):
    if value <= timezone.now().date():
        raise ValidationError("Please enter a future date")


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    description = models.TextField()
    dateEnd = models.DateField(default=timezone.now)
    status = models.IntegerField(choices=STATUS, default=1)
    user = models.ForeignKey("UserStaff", on_delete=models.CASCADE,null=True,blank=True)
    team = models.ForeignKey("Team", on_delete=models.CASCADE,null=True,blank=True)
    def clean(self):
        if self.dateEnd is not None and self.dateEnd <= timezone.now().date():
            raise ValidationError({'dateEnd': "Please enter a future date."})
    def __str__(self):
        return self.title

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    manager = models.ForeignKey("UserStaff", on_delete=models.CASCADE,null=True,blank=True,related_name="managed_team")
    def __str__(self):
        return self.name

