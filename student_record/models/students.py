from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from student_record.errors import InvalidScoreError, InvalidSubjectError
from student_record.models.classes import Class
from student_record.models.subjects import Subject


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    roll = models.IntegerField(unique=True)
    class_id = models.ForeignKey(
        Class,
        verbose_name="class",
        on_delete=models.CASCADE,
        null=True,
        related_name="students",
        db_column="class",
    )
    subjects = models.ManyToManyField(Subject, through="StudentSubject")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        subjects = self.class_id.subjects.filter(is_elective=False)
        self.subjects.add(*subjects)


class StudentSubject(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="scores"
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
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
    total = models.FloatField(null=True, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint("subject", "student", name="unique_student_subject")
        ]

    def total_marks(self):
        return self.th + self.pr if self.pr else self.th

    def validate_marks(self, obtain, total, source):
        if total and obtain is None:
            obtain = 0
        if not total and obtain:
            raise InvalidScoreError(f"Subject has no {source} marks.")
        if all([obtain, total]) and obtain > total:
            raise InvalidScoreError(
                f"{source.title()}: Obtained Marks cannot be greater than Total Marks"
            )

    def validate_subject(self):
        if self.subject not in self.student.class_id.subjects.all():
            raise InvalidSubjectError(
                "Invalid Subject. Add Subject associated with particular class."
            )

    def clean(self) -> None:
        subject_marks = self.subject.marks
        self.validate_marks(self.th, subject_marks.theory, "theory")
        self.validate_marks(self.pr, subject_marks.practical, "practical")
        self.validate_subject()
        return super().clean()

    def save(self, *args, **kwargs) -> None:
        self.total = self.total_marks
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.student} - {self.subject}"


class MarkSheet(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_id = models.ForeignKey(
        Class, verbose_name=_("Class"), on_delete=models.CASCADE
    )
    exam_type = models.CharField(max_length=100, default="board")
    total_marks = models.FloatField()
    percentage = models.FloatField()
    status = models.CharField(
        max_length=100,
        choices=[("PASS", "PASS"), ("FAIL", "FAIL")],
    )
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{str(self.student)}:{self.percentage}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "class_id", "exam_type"], name="unique_marksheet"
            )
        ]
