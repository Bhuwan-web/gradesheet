from django.db import models
from django.core.validators import MinValueValidator


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
