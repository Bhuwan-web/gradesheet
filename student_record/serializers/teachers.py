from rest_framework import serializers
from student_record.models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["first_name", "last_name"]
