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
    Choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            'paper',
            'type',
            'content',
            'type',
            'choices'
        )


class PaperSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            'title',
            'content',
            'deadline',
            'preview_image',
            'questions'
        )

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', None)
        paper = Paper.objects.create(**validated_data)
        if questions_data:
            for question_data in questions_data:
                choices_data = question_data.pop('choices', None)
                question = Question.objects.create(**question_data)
                if choices_data:
                    for choice_data in choices_data:
                        Choice.objects.create(question=question, **choices_data)
        return paper
