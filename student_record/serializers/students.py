from rest_framework import serializers
from student_record.models import Student, Subject
from student_record.serializers.student_subjects import (
    ListStudentSubjectSerializer,
    StudentSubjectSerializer,
)


class CreateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "roll", "grade", "section"]


class StudentListSerializer(serializers.ModelSerializer):
    scores = ListStudentSubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ["first_name", "last_name", "roll", "scores"]


class StudentSerializer(serializers.ModelSerializer):
    subjects = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Subject.objects.all()
    )

    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "roll",
            "student_class",
            "subjects",
            "scores",
        ]


class StudentMarksEntrySerializer(serializers.ModelSerializer):
    scores = ListStudentSubjectSerializer(many=True)
    roll = serializers.IntegerField()

    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "roll",
            "student_class",
            "scores",
        ]
