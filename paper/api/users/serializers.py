from rest_framework import serializers
from apps.users.models import PaperUser

class PaperuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperUser
        exclude = ('is_staff', 'is_superuser', 'password')
        read_only_fields = (
            'joined_date',
        )  # auto_now_add나 auto_now가 true이면 read_only_fields여야 함.


class PaperuserListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PaperUser
        fields = (
            'id',
            'email',
            'url',
            'nickName',
            'profile_image',
        )
