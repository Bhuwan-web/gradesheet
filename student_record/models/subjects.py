from django.db import models
from django.core.validators import MinValueValidator
from student_record.models.teachers import Teacher


# create a model for pass and full marks that will relate to marks model
class MarksClassification(models.Model):
    pass_marks = models.FloatField(validators=[MinValueValidator(0)])
    full_marks = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self) -> str:
        return f"{self.full_marks}:{self.pass_marks}"


class Marks(models.Model):
    theory = models.ForeignKey(
        MarksClassification,
        on_delete=models.CASCADE,
        related_name="theory",
    )
    practical = models.ForeignKey(
        MarksClassification,
        on_delete=models.CASCADE,
        related_name="practical",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return (
            f"TH - {self.theory} / PR -{self.practical}"
            if self.practical
            else f"TH - {self.theory}"
        )


class Subject(models.Model):
    subject_code = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=100)
    marks = models.ForeignKey(Marks, on_delete=models.CASCADE)
    credit_hours = models.FloatField()
    is_elective = models.BooleanField(default=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}({self.subject_code})"
