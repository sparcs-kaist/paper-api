from django.db import models
from apps.papers.models import Paper, Question, Choice
from apps.common.models import TimeStampedModel, HavingAuthorModel


# Create your models here.

class Participate(TimeStampedModel, HavingAuthorModel):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)


class Answer(models.Model):
    participate = models.ForeignKey(Participate, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True, default=None) # blank= true , null = true면 optional이다.

    class Meta:
        order_with_respect_to = 'participate'

class Select(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, blank=True, null=True, default=None) # blank= true , null = true면 optional이다.
