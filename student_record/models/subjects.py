from django.db import models
from django.core.validators import MinValueValidator
from student_record.models.teachers import Teacher


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
