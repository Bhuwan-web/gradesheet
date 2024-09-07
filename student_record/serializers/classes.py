from rest_framework import serializers
from student_record.models import Class
from student_record.serializers.students import StudentListSerializer


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ["graduation_year", "grade", "section", "class_teacher"]


class ClassResultSerializer(serializers.ModelSerializer):
    students = StudentListSerializer(many=True, read_only=True)
    class_teacher = serializers.StringRelatedField()

    class Meta:
        model = Class
        fields = [
            "graduation_year",
            "grade",
            "section",
            "class_teacher",
            "students",
        ]
