from rest_framework import serializers
from student_record.models import StudentSubject, Subject


class StudentSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubject
        fields = ["student", "subject", "th", "pr"]


class ListStudentSubjectSerializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField()

    class Meta:
        model = StudentSubject
        fields = ["subject", "th", "pr"]
