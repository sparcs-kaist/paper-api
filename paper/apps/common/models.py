from django.db import models
from apps.users.models import PaperUser


class TimeStampedModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class HavingAuthorModel(models.Model):
    author = models.ForeignKey(
        PaperUser, on_delete=models.CASCADE, default=None
    )

    class Meta:
        abstract = True
