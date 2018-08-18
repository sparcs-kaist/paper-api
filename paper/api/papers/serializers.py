from rest_framework import serializers
from api.users.serializers import PaperuserSerializer, PaperuserListSerializer
from apps.papers.models import Paper, Question, Choice
# from api.answers.serializers import ParticipateSerializer
import json


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            'paper',
            'content',
            'type',
            'choices',
            'is_multiple'
        )


class BriefQuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            'type',
            'content',
            'is_multiple',
            'choices'
        )


class PaperCreateSerializer(serializers.ModelSerializer):
    # questions = QuestionSerializer(many=True)

    class Meta:
        model = Paper
        fields = (
            'title',
            'content',
            'deadline',
            'preview_image',
            'poster_url',
            # 'questions',
        )

    def to_internal_value(self, data):
        instance = super(PaperCreateSerializer, self).to_internal_value(data)
        if "questions" in data:
            questions_str_data = data["questions"]
            questions_json = json.loads(questions_str_data)
            instance["questions"] = questions_json
        return instance

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', None)
        paper = Paper.objects.create(**validated_data)
        if questions_data:
            for question_data in questions_data:
                choices_data = question_data.pop('choices', None)
                question = Question.objects.create(paper=paper, **question_data)
                if choices_data:
                    for choice_data in choices_data:
                        Choice.objects.create(question=question, **choice_data)
        return paper


class PaperSerializer(serializers.ModelSerializer):
    author = PaperuserListSerializer(read_only=True)
    preview_image_thumbnail = serializers.ImageField(read_only=True)
    questions = QuestionSerializer(read_only=True, many=True)

    class Meta:
        model = Paper
        fields = (
            'id',
            'title',
            'content',
            'deadline',
            'poster_url',
            'preview_image',
            'preview_image_thumbnail',
            'questions',
            'author',
        )
        read_only_fields = (
            'created_time',
            'updated_time',
        )


class PaperListSerializer(serializers.ModelSerializer):
    preview_image_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = Paper
        fields = (
            'id',
            'title',
            'deadline',
            'poster_url',
            'preview_image_thumbnail',
        )
        read_only_fields = (
            'created_time',
            'updated_time',
        )
