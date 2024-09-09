from django.db import models
from student_record.models.teachers import Teacher
from student_record.models.subjects import Subject


class Class(models.Model):
    graduation_year = models.IntegerField()
    class_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    grade = models.IntegerField()
    section = models.CharField(max_length=64, default=None, null=True, blank=True)
    subjects = models.ManyToManyField(
        Subject, related_name="classes", through="ClassSubject"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint("grade", "section", name="unique_class"),
        ]

    def __str__(self):
        return f"{self.graduation_year} - {self.grade}'{self.section}'"


class ClassSubject(models.Model):
    class_ = models.ForeignKey(Class, verbose_name="class", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.class_} - {self.subject}"
