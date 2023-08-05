from rest_framework import serializers
from ocr_api.models import OcrModel


class OcrSerializer(serializers.ModelSerializer):
    class Meta:
        model = OcrModel
        fields = '__all__'
