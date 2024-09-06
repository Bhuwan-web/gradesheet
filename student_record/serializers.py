from rest_framework import serializers
from .models import Student, Subject, StudentSubject


class CreateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "roll", "grade", "section"]
