from rest_framework import generics

from student_record import models, serializers


class ListCreateSubject(generics.ListCreateAPIView):
    queryset = models.Subject.objects.select_related("teacher", "marks").all()
    serializer_class = serializers.SubjectSerializer


class ListCreateTeacher(generics.ListCreateAPIView):
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer


class ListCreateStudent(generics.ListCreateAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer


class ListCreateClass(generics.ListCreateAPIView):
    queryset = models.Class.objects.all()
    serializer_class = serializers.ClassSerializer


class ListCreateStudentSubject(generics.ListCreateAPIView):
    queryset = models.StudentSubject.objects.all()
    serializer_class = serializers.StudentSubjectSerializer


class ListClassResult(generics.ListAPIView):
    queryset = models.Class.objects.prefetch_related("students").all()
    serializer_class = serializers.ClassResultSerializer
