from django.urls import path

from . import views

urlpatterns = [
    path("subjects/", views.ListCreateSubject.as_view(), name="subject"),
    path("teachers/", views.ListCreateTeacher.as_view(), name="teacher"),
    path("students/", views.ListCreateStudent.as_view(), name="student"),
    path(
        "students-subjects/",
        views.ListCreateStudentSubject.as_view(),
        name="student_subject",
    ),
    path("classes/", views.ListCreateClass.as_view(), name="class"),
    path("class-results/", views.ListClassResult.as_view(), name="class_result"),
]
