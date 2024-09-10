from django.contrib import admin
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
