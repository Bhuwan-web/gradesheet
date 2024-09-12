from django import forms
from .models.students import MarkSheet, StudentSubject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = StudentSubject
        fields = "__all__"


StudentSubjectFormSet = forms.modelformset_factory(
    StudentSubject, form=SubjectForm, extra=3
)


class MarkSheetForm(forms.ModelForm):
    student_subjects = StudentSubjectFormSet(queryset=StudentSubject.objects.all())

    class Meta:
        model = MarkSheet
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # if self.instance.pk:
        #     student_subjects = self.instance.student.scores.all()
        #     self.fields["subjects"].queryset = student_subjects

        #     self.fields["subjects"].initial = student_subjects
