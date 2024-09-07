from rest_framework import serializers
from student_record.models import Marks, Subject, Teacher
from student_record.serializers.marks import MarksSerializer


class SubjectSerializer(serializers.ModelSerializer):
    marks = MarksSerializer()

    class Meta:
        model = Subject
        fields = [
            "name",
            "subject_code",
            "credit_hours",
            "teacher",
            "marks",
        ]
        # depth = 1

    # def get_teacher_name(self, obj: Subject):
    #     return f"{obj.teacher.first_name} {obj.teacher.last_name}"

    def create(self, validated_data):
        marks_data = validated_data.pop("marks")
        teacher_data = validated_data.pop("teacher")
        marks_obj = Marks.objects.get_or_create(**marks_data)
        teacher_obj = Teacher.objects.get_or_create(**teacher_data)
        subject = Subject.objects.create(
            **validated_data, marks=marks_obj[0], teacher=teacher_obj[0]
        )
        return subject
