from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from student_record.models.classes import Class, ClassSubject
from student_record.models.subjects import Subject
from student_record.errors import InvalidScoreError


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    roll = models.IntegerField(unique=True)
    student_class = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        null=True,
        related_name="students",
        db_column="class",
    )
    subject_scores = models.ManyToManyField(Subject, through="StudentSubject")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StudentSubject(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="scores"
    )
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE)
    th = models.FloatField(
        _("Theory Marks"),
        validators=[MinValueValidator(0)],
        default=0,
    )
    pr = models.FloatField(
        _("Practical Marks"),
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        default=None,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint("subject", "student", name="unique_student_subject")
        ]

    def total_marks(self):
        if self.pr:
            return self.th + self.pr
        return self.th

    def validate_marks(self, obtain, total, source):
        if total and obtain is None:
            raise InvalidScoreError(f"Obtained Marks cannot be empty for {source}.")
        if not total and obtain:
            raise InvalidScoreError(f"Subject has no {source} marks.")
        if all([obtain, total]) and obtain > total:
            raise InvalidScoreError(
                f"{source.title()}: Obtained Marks cannot be greater than Total Marks"
            )

    def clean(self) -> None:
        subject_marks = self.class_subject.subject.marks
        self.validate_marks(self.th, subject_marks.theory, "theory")
        self.validate_marks(self.pr, subject_marks.practical, "practical")
        return super().clean()

    def __str__(self) -> str:
        return f"{self.student} - {self.subject}"
