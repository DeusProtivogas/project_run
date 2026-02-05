from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class Run(models.Model):
    class Meta:
        verbose_name = f'Забеги'

    STATUS_CHOICES = [
        ('init', 'начат'),
        ('in_progress', 'в процессе'),
        ('finished', 'завершен'),
    ]

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    athlete = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    comment = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='init',
    )

    def __str__(self):
        return f'ID {self.id} - {self.athlete.username} - {self.status}'


class AthleteInfo(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    weight = models.IntegerField(
        null=True,
    )
    goal = models.TextField(
        max_length=200,
        blank=True,
    )

