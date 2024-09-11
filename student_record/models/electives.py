from django.core.exceptions import ValidationError
from django.db import models

from student_record.models.classes import Class
from student_record.models.students import Student
from student_record.models.subjects import Subject


class ElectiveGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ElectiveStudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    elective_group = models.ForeignKey(ElectiveGroup, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student} - {self.elective_group}:{self.subject}"

    def clean(self) -> None:
        self.student.subjects.add(self.subject)
        super().clean()


class ElectiveSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    elective_group = models.ForeignKey(ElectiveGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject} - {self.elective_group}"

    def clean(self) -> None:
        subject_obj = self.subject
        if not subject_obj.is_elective:
            raise ValidationError("Subject is not an Elective Subject")
        return super().clean()


class ElectiveClass(models.Model):
    elective_group = models.ForeignKey(ElectiveGroup, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, verbose_name="class", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.elective_group}: - {self.class_id}"
