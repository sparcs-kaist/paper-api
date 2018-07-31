from django.db import models
from apps.common.models import TimeStampedModel
from apps.users.models import PaperUser

class PaperMail(TimeStampedModel):
    sender =  models.ForeignKey(PaperUser, on_delete=models.CASCADE, related_name="paper_mails")
    receivers = models.ManyToManyField(PaperUser)
    subject = models.CharField(max_length=140, default="Title")
    message = models.TextField(blank=True, null=True)

