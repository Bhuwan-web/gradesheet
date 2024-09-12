from django.db.models import Sum
from rest_framework import serializers
from student_record.models.classes import Class
from student_record.models.students import MarkSheet, Student
from django.db import transaction


class MarkSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkSheet
        fields = "__all__"


class CreateMarkLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkSheet
        fields = ["class_id"]

    def create(self, validated_data):
        class_obj: Class = validated_data["class_id"]
        students: list[Student] = class_obj.students.prefetch_related(
            "subjects__marks", "scores"
        )
        mark_sheet_records = []
        for student in students:
            total_obtained = student.scores.aggregate(total=Sum("total"))["total"]
            total_marks = student.subjects.aggregate(
                total=Sum("marks__theory__full_marks")
                + Sum("marks__practical__full_marks")
            )["total"]
            percentage = round((total_obtained / total_marks) * 100, 2)
            status = "PASS" if percentage >= 40 else "FAIL"
            mark_sheet_records.append(
                {
                    "student": student,
                    "class_id": class_obj,
                    "total_marks": total_marks,
                    "percentage": percentage,
                    "status": status,
                }
            )
        with transaction.atomic():
            MarkSheet.objects.bulk_create(
                [MarkSheet(**record) for record in mark_sheet_records],
                update_conflicts=True,
                update_fields=["total_marks", "percentage", "status"],
                unique_fields=["student", "class_id", "exam_type"],
            )
        return MarkSheet.objects.filter(class_id=class_obj).first()
