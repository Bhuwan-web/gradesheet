from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from student_record.models import StudentSubject, Subject


class StudentSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubject
        fields = ["student", "subject", "th", "pr"]


class ListStudentSubjectSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source="subject.subject_code")

    class Meta:
        model = StudentSubject
        fields = ["subject", "th", "pr"]
