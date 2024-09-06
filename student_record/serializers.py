from rest_framework import serializers
from .models import Student, Subject, StudentSubject, Teacher, Class, Marks


class CreateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "roll", "grade", "section"]


class MarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marks
        fields = ["theory", "practical"]


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["first_name", "last_name"]


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


class StudentSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubject
        fields = ["student", "subject", "th", "pr"]


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ["graduation_year", "grade", "section", "class_teacher"]


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
            "studentsubject_set",
        ]


class StudentListSerializer(serializers.ModelSerializer):
    studentsubject_set = StudentSubjectSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ["first_name", "last_name", "roll", "studentsubject_set"]


class ClassResultSerializer(serializers.ModelSerializer):
    students = StudentListSerializer(many=True, read_only=True)

    class Meta:
        model = Class
        fields = [
            "graduation_year",
            "grade",
            "section",
            "class_teacher",
            "students",
        ]
