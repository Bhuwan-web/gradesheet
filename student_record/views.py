from rest_framework import generics
from django.db.models import Prefetch
from student_record import models
from student_record.serializers import (
    classes,
    marks,
    subjects,
    teachers,
    students,
    student_subjects,
)


class ListCreateSubject(generics.ListCreateAPIView):
    queryset = models.Subject.objects.select_related("teacher", "marks").all()
    serializer_class = subjects.SubjectSerializer


class ListCreateTeacher(generics.ListCreateAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = teachers.TeacherSerializer


class ListCreateStudent(generics.ListCreateAPIView):
    queryset = models.Student.objects.all()
    serializer_class = students.StudentSerializer


class ListCreateClass(generics.ListCreateAPIView):
    queryset = models.Class.objects.all()
    serializer_class = classes.ClassSerializer


class ListCreateStudentSubject(generics.ListCreateAPIView):
    queryset = models.StudentSubject.objects.all()
    serializer_class = students.StudentSubjectSerializer


class ListClassResult(generics.ListAPIView):
    queryset = models.Class.objects.select_related("class_teacher").prefetch_related(
        Prefetch(
            "students",
            models.Student.objects.prefetch_related(
                Prefetch(
                    "scores",
                    models.StudentSubject.objects.prefetch_related(
                        Prefetch("subject", models.Subject.objects.only("name"))
                    ),
                )
            ),
        )
    )
    serializer_class = classes.ClassResultSerializer
