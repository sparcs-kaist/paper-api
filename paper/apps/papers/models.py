from django.db import models
from apps.users.models import PaperUser
from apps.common.models import TimeStampedModel, HavingAuthorModel


class Paper(TimeStampedModel, HavingAuthorModel):
    title = models.CharField(max_length=50, default="Title")
    content = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(editable=True, default=None)
    is_deleted = models.BooleanField(deafault=False)
    is_validated = models.BooleanField(default=False)


class Question(models.Model):
    QUESTION_TYPE = (
        ('C', 'Checkbox'),
        ('R', 'Radio'),
        ('O', 'Open-Ended')
    )
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    content = models.CharField(max_length=140, default="empty question")
    type = models.CharField(
        max_length=1, choices=QUESTION_TYPE
    )
    is_multiple = models.BooleanField(default=False)

    class Meta:
        order_with_respect_to = 'paper'


class Choice(models.model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.CharField(max_length=50, default="option")

    class Meta:
        order_with_respect_to = 'question'
