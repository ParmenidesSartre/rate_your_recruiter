from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    company = models.ForeignKey(
        'reviews.Company', on_delete=models.SET_NULL, null=True, blank=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
