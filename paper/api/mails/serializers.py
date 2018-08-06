from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from api.users.serializers import PaperuserSerializer, PaperuserListSerializer
from apps.mails.models import PaperMail
import json



class PaperMailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperMail
        fields = '__all__'

    def to_internal_value(self, data):
        instance = super(PaperMailCreateSerializer, self).to_internal_value(data)
        if "receivers_address" in data:
            receivers_data = data["receivers_address"]
            instance["receivers_address"] = ':'.join(receivers_data)
        return instance

