from django.core.exceptions import ValidationError


class InvalidScoreError(ValidationError):
    pass


class InvalidSubjectError(ValidationError):
    pass
