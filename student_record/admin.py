from django.contrib import admin
from . import models
# Register your models here.


class StudentSubjectAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "subject",
        "th",
        "pr",
        "total_marks",
    )


class SubjectInline(admin.TabularInline):
    model = models.Subject
    extra = 3


class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [SubjectInline]


class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "subject_code",
        "teacher__name",
        "name",
        "marks__theory",
        "marks__practical",
        "credit_hours",
    )


admin.site.register(models.Student)
admin.site.register(models.Subject, SubjectAdmin)
admin.site.register(models.Teacher, TeacherAdmin)
admin.site.register(models.StudentSubject, StudentSubjectAdmin)
