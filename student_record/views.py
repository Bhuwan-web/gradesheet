from operator import ge
import django_filters
from rest_framework import generics
from django.db.models import Prefetch
from student_record import models
from student_record.serializers import (
    classes,
    subjects,
    teachers,
    students,
)
from rest_framework.response import Response


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
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


class RetrieveClassResultAPIView(generics.RetrieveDestroyAPIView):
    queryset = models.Class.objects.select_related("class_teacher").prefetch_related(
        Prefetch(
            "students",
            models.Student.objects.prefetch_related(
                Prefetch(
                    "scores",
                    models.StudentSubject.objects.select_related("subject"),
                )
            ),
        )
    )
    serializer_class = classes.ClassResultSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


class RetrieveUpdateDeleteStudent(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Student.objects.prefetch_related(
        Prefetch(
            "scores",
            models.StudentSubject.objects.select_related("subject").only(
                "subject", "th", "pr", "student"
            ),
        )
    )
    serializer_class = students.StudentListSerializer


class CreateClassMarksEntry(generics.UpdateAPIView):
    queryset = models.Class.objects
    serializer_class = classes.ClassMarksEntry

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class ClassMarkLedgerCSV(generics.CreateAPIView):
    model = models.Class
    serializer_class = classes.ClassMarkLedgerCSVSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)
