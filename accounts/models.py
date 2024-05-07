from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20, choices=(
        ('employee', 'Employee'), ('manager', 'Manager')), default='employee')
    company = models.ForeignKey(
        'reviews.Company', on_delete=models.SET_NULL, null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
