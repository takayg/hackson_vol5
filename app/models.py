from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):

    user = models.ForeignKey(
        to=User,
        verbose_name='User',
        on_delete=models.CASCADE
    )

    start_time = models.DateField(
        verbose_name='start_time'
    )

    finish_time = models.DateField(
        verbose_name='finish_time'
    )

    class Meta:
        verbose_name_plural='Activity'

class ActivityDetail(models.Model):

    activity = models.ForeignKey(
        to=Activity,
        verbose_name='Activity',
        on_delete=models.CASCADE
    )

    rest_start_time = models.DateField(
        verbose_name='rest_start_time',
    )

    rest_finish_time = models.DateField(
        verbose_name='rest_finish_time'
    )

