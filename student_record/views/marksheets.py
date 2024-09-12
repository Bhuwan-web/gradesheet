from rest_framework import generics

from student_record.models.students import MarkSheet
from student_record.serializers import marksheets


class CreateMarkLedger(generics.CreateAPIView):
    queryset = MarkSheet.objects.all()
    serializer_class = marksheets.CreateMarkLedgerSerializer
