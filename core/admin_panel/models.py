from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import User

class Log(models.Model):
  account = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs')
  msg = models.CharField(max_length=150)
  action_type = models.CharField(max_length=50, choices=[
    ('AUTH', 'Authentication action type'),
    ('CREATE', 'create object in the db'),
    ('READ', 'read object in the db'),
    ('UPDATE', 'update object in the db'),
    ('DELETE', 'delete object in the db'),
    ('PREDICT', 'use the COVID prediction api'),
  ]),
  success = models.BooleanField(default=True),
  created_at = models.DateTimeField(auto_now_add=True)
