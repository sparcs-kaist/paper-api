from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.users.serializers import PaperuserSerializer
from apps.papers.models import Paper, Question, Choice
from django.conf import settings
import json


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    Choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            'paper',
            'type',
            'content',
            'type',
            'choices'
        )

    def create(self, validated_data):
        choices_data = validated_data.pop('choices', None)
        question = Question.objects.create(**validated_data)
        if choices_data:
            for choice_data in choices_data:
                Choice.objects.create(question=question, **choices_data)
        return question




