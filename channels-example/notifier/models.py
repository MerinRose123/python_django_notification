from django.conf import settings
from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import AbstractUser

'''
class User(AbstractUser):
    address = models.CharField(max_length=80,null=True, blank=True)
'''


class Like(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

