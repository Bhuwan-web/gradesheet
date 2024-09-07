from rest_framework import serializers
from student_record.models import Marks


class MarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marks
        fields = ["theory", "practical"]
