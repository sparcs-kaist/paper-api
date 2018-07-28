from django.shortcuts import get_object_or_404
from rest_framework import serializers
from api.users.serializers import PaperuserSerializer, PaperuserListSerializer
from api.papers.serializers import PaperListSerializer, ChoiceSerializer, QuestionSerializer
from apps.papers.models import Paper, Question, Choice
from apps.answers.models import Participate, Answer, Select
from django.core.exceptions import ObjectDoesNotExist
import json


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    choice = ChoiceSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = (
            'question',
            'select'
            'content'
        )


class ParticipateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participate
        fields = (
            'paper',
        )

    def to_internal_value(self, data):
        instance = super(ParticipateCreateSerializer, self).to_internal_value(data)
        if "answers" in data:
            answers_str_data = data["answers"]
            answers_json = json.loads(answers_str_data)
            instance["answers"] = answers_json
        return instance

    def create(self, validated_data):
        answers_data = validated_data.pop('answers', None)
        try:
            participate = Participate.objects.create(**validated_data)
            if answers_data:
                questions = Question.objects.filter(paper=participate.paper)
                for answer_data, question in zip(answers_data, questions):
                    if question.type == 'C' or question.type == 'R':
                        choice_id_list = Choice.objects.filter(question=question).values_list('id', flat=True)
                        if answer_data["selects"] is None:
                            raise AssertionError()
                        selects_data = answer_data.pop('selects')
                        if question.is_multiple == False and len(selects_data) > 1:
                            raise AssertionError()
                        answer = Answer.objects.create(participate=participate, question=question, **answer_data)
                        for select_data in selects_data:
                            select_choice_id = select_data["choice"]
                            if select_choice_id not in choice_id_list:
                                raise AssertionError()
                            choice = Choice.objects.get(id=select_data["choice"])
                            Select.objects.create(answer=answer, choice=choice)
                    elif question.type == 'O':
                        if answer_data["content"] is None:
                            raise AssertionError()
                        Answer.objects.create(participate=participate, question=question, **answer_data)
        except ObjectDoesNotExist or AssertionError:
            participate.delete()
        return participate


class ParticipateSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    author = PaperuserListSerializer(read_only=True)
    paper = PaperListSerializer(read_only=True)

    class Meta:
        model = Participate
        fields = (
            'id',
            'paper',
            'answers',
            'author',
        )
        read_only_fields = (
            'created_time',
            'updated_time',
        )


class ParticipateListSerializer(serializers.ModelSerializer):
    paper = PaperListSerializer(many=True, read_only=True)

    class Meta:
        model = Participate
        fields = (
            'id',
            'paper'
        )
        read_only_fields = (
            'created_time',
            'updated_time',
        )
