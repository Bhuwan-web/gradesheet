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


class StudentInline(admin.TabularInline):
    model = models.Student
    extra = 3


class SubjectInline(admin.TabularInline):
    model = models.Subject
    extra = 3


class TeacherAdmin(admin.ModelAdmin):
    inlines = [SubjectInline]


class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "subject_code",
        "teacher",
        "name",
        "marks__theory",
        "marks__practical",
        "credit_hours",
    )


class ClassAdmin(admin.ModelAdmin):
    list_display = ("graduation_year", "grade", "section", "class_teacher")

    inlines = [StudentInline]


admin.site.register(models.Student)
admin.site.register(models.Subject, SubjectAdmin)
admin.site.register(models.Teacher, TeacherAdmin)
admin.site.register(models.StudentSubject, StudentSubjectAdmin)
admin.site.register(models.Marks)
admin.site.register(models.Class, ClassAdmin)
