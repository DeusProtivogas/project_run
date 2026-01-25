from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class Run(models.Model):
    started_at = models.DateTimeField(
        auto_now_add=True
    )
    athlete = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    comment = models.TextField()