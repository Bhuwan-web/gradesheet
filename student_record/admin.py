from django.contrib import admin
from student_record.marksheet_admin_view import MarkSheetForm
from student_record.models import students, classes, subjects, teachers, electives
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
    model = students.Student
    extra = 3


class SubjectInline(admin.TabularInline):
    model = subjects.Subject
    extra = 3


class ElectiveStudentSubjectInline(admin.TabularInline):
    model = electives.ElectiveStudentSubject
    extra = 3
    # collapse
    classes = {"collapse": True}


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


class ClassSubjectInline(admin.StackedInline):
    model = classes.ClassSubject
    extra = 3
    classes = {"collapse": False}


class ClassAdmin(admin.ModelAdmin):
    list_display = ("graduation_year", "grade", "section", "class_teacher")
    model = classes.Class
    inlines = [ClassSubjectInline, StudentInline]


class StudentSubjectClassInline(admin.TabularInline):
    model = students.StudentSubject
    extra = 3
    classes = {"collapse": True}


class StudentAdmin(admin.ModelAdmin):
    inlines = [ElectiveStudentSubjectInline, StudentSubjectClassInline]

    list_display = ("first_name", "last_name", "roll", "class_id")


class ElectiveSubjectInline(admin.TabularInline):
    list_display = ("subject", "elective_group")
    model = electives.ElectiveSubject


# class MarkSheetAdmin(admin.ModelAdmin):
#     list_display = ("student", "class_id", "percentage", "status")
#     list_filter = ("status", "class_id")
#     readonly_fields = ("percentage", "status")
#     ordering = ("student__roll",)
#     form = MarkSheetForm
#     fields = ("student", "class_id", "percentage", "status", "student_subjects")
#     # fieldsets = (
#     #     (
#     #         "Summary",
#     #         {"fields": ("student", "class_id", "percentage", "status", "subjects")},
#     #     ),
#     # )

#     # inlines = [StudentSubjectClassInline]
#     ...


class MarkSheetAdmin(admin.ModelAdmin):
    list_display = ("student", "class_id", "percentage", "status")
    change_form_template = "admin/marksheet_change_form.html"

    # Custom method to pass the subject-wise scores to the template
    def render_change_form(self, request, context, *args, **kwargs):
        obj = kwargs.get("obj")

        if obj:
            # Get all StudentSubject entries for the related student
            student_subjects = students.StudentSubject.objects.filter(
                student=obj.student
            )
            context["subject_scores"] = student_subjects  # Pass to the template

        return super().render_change_form(request, context, *args, **kwargs)


class ElectiveAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [ElectiveSubjectInline]


admin.site.register(electives.ElectiveGroup, ElectiveAdmin)
admin.site.register(students.Student, StudentAdmin)
admin.site.register(subjects.Subject, SubjectAdmin)
admin.site.register(teachers.Teacher, TeacherAdmin)
# admin.site.register(students.StudentSubject, StudentSubjectAdmin)
admin.site.register(subjects.Marks)
admin.site.register(classes.Class, ClassAdmin)
# admin.site.register(electives.ElectiveSubject, ElectiveSubjectAdmin)
admin.site.register(students.MarkSheet, MarkSheetAdmin)
