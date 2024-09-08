from rest_framework import serializers
from student_record.models import Class, Student, StudentSubject, Subject
from student_record.serializers.students import (
    StudentListSerializer,
    StudentMarksEntrySerializer,
)
from django.db import transaction


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


class ClassMarksEntry(serializers.ModelSerializer):
    students = StudentMarksEntrySerializer(many=True)

    class Meta:
        model = Class
        fields = ["graduation_year", "students", "grade", "section"]

    def get_or_create_class_instance(self, validated_data):
        try:
            class_obj, _ = Class.objects.filter(
                grade=validated_data["grade"], section=validated_data["section"]
            ).first()
        except Class.DoesNotExist:
            class_obj = Class.objects.create(**validated_data)
        finally:
            return class_obj

    def get_or_create_student_instance(self, student_data):
        try:
            student_obj = Student.objects.get(roll=student_data["roll"])
        except Student.DoesNotExist:
            student_obj = Student.objects.create(**student_data)
        finally:
            return student_obj

    def get_subject_instance(self, subject_data):
        try:
            subject_obj = Subject.objects.get(subject_code=subject_data["subject_code"])
        except Subject.DoesNotExist:
            serializers.ValidationError("Subject Does Not Exist")
        finally:
            return subject_obj

    def add_scores(self, student_obj, subject_obj, score):
        obj, created = StudentSubject.objects.get_or_create(
            student=student_obj, subject=subject_obj, defaults=score
        )
        if not created:
            obj.th = score["th"]
            obj.pr = score["pr"]
            obj.save()

    def update(self, instance, validated_data):
        students_data = validated_data.pop("students")
        with transaction.atomic():
            class_obj = instance
            for student_data in students_data:
                scores = student_data.pop("scores")
                student_data["student_class"] = class_obj
                student_obj = self.get_or_create_student_instance(student_data)
                for score in scores:
                    subject_data = score.pop("subject")
                    subject_obj = self.get_subject_instance(subject_data)
                    self.add_scores(student_obj, subject_obj, score)
        return class_obj


class ClassMarkLedgerCSVSerializer(serializers.Serializer):
    class_details = ClassSerializer()
    mark_ledger = serializers.FileField()
