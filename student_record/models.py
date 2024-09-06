from django.db import models
from django.utils.translation import gettext_lazy as _

from student_record.errors import InvalidScoreError
from django.core.validators import MinValueValidator


# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    roll = models.IntegerField(unique=True)
    grade = models.IntegerField()
    section = models.CharField(max_length=64, default=None, null=True, blank=True)
    subjects = models.ManyToManyField("Subject", through="StudentSubject")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Teacher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Marks(models.Model):
    theory = models.FloatField(validators=[MinValueValidator(0)])
    practical = models.FloatField(
        default=None, null=True, blank=True, validators=[MinValueValidator(0)]
    )

    def __str__(self) -> str:
        return (
            f"TH: {self.theory}, PR:{self.practical}"
            if self.practical
            else f"TH: {self.theory}"
        )


class Subject(models.Model):
    subject_code = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=100)
    marks = models.ForeignKey(Marks, on_delete=models.CASCADE)
    credit_hours = models.FloatField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class StudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    th = models.FloatField(
        _("Theory Marks"),
        validators=[MinValueValidator(0)],
    )
    pr = models.FloatField(
        _("Practical Marks"),
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        default=None,
    )

    def total_marks(self):
        if self.pr:
            return self.th + self.pr
        return self.th

    def validate_marks(self, obtain, total):
        if total and not obtain:
            raise InvalidScoreError("Obtained Marks cannot be empty")
        if all([obtain, total]) and obtain > total:
            raise InvalidScoreError("Obtained Marks cannot be greater than Total Marks")

    def clean(self) -> None:
        self.validate_marks(self.th, self.subject.marks.theory)
        self.validate_marks(self.pr, self.subject.marks.practical)
        return super().clean()

    def __str__(self) -> str:
        return f"{self.student} - {self.subject}"
