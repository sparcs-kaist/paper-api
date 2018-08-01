from rest_framework import serializers
from api.users.serializers import PaperuserListSerializer
from apps.papers.models import Paper
from api.answers.serializers import CheckingParticipateSerializer
from .serializers import QuestionSerializer


class PaperAdminSerializer(serializers.ModelSerializer):
    author = PaperuserListSerializer(read_only=True)
    preview_image_thumbnail = serializers.ImageField(read_only=True)
    questions = QuestionSerializer(read_only=True, many=True)
    participates = CheckingParticipateSerializer(read_only=True, many=True)

    class Meta:
        model = Paper
        fields = (
            'id',
            'title',
            'content',
            'deadline',
            'preview_image',
            'preview_image_thumbnail',
            'questions',
            'author',
            'participates',
        )
        read_only_fields = (
            'created_time',
            'updated_time',
        )
