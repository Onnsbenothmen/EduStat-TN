from rest_framework import serializers
from .models import OrientationRecord


class OrientationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrientationRecord
        fields = "__all__"
