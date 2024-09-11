from rest_framework import serializers
from student_record.models.students import Student


class MarkSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
