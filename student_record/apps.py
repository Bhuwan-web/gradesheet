from django.apps import AppConfig


class StudentRecordConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "student_record"

    def ready(self):
        import student_record.signals
