# dashboard/models.py
from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    ROLE_CHOICES = [
    ('fullstack', 'Full Stack Developer'),
    ('frontend', 'Frontend Developer'),
    ('backend', 'Backend Developer'),
    ('mobile', 'Mobile Developer'),
    ('designer', 'UI/UX Designer'),
    ('editor', 'Video / Photo Editor'),
  ]


  
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username
