from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models import F, Min
from student_record.models.electives import (
    ElectiveClass,
    ElectiveStudentSubject,
    ElectiveSubject,
)
from student_record.models.students import Student


def unique_subject_elective(data):
    unique_elective_subjects = []

    def is_unique(element):
        if (eg := element["elective_group_id"]) not in unique_elective_subjects:
            unique_elective_subjects.append(eg)
            return True

    return filter(lambda x: is_unique(x), data)


@receiver(pre_save, sender=ElectiveSubject)
def elective_subject_save(sender, instance: ElectiveSubject, **kwargs):
    classes = instance.subject.classes.all()
    ElectiveClass.objects.bulk_create(
        [
            ElectiveClass(elective_group=instance.elective_group, class_id=class_id)
            for class_id in classes
        ]
    )


@receiver(post_save, sender=Student)
def student_save(sender, instance: Student, created, **kwargs):
    if created:
        elective_subject_groups = (
            instance.class_id.subjects.filter(is_elective=True)
            .annotate(
                elective_group_id=F("electivesubject__elective_group"),
                subject_id=Min("electivesubject__subject"),
            )
            .values("elective_group_id", "subject_id")
            .distinct()
        )
        elective_subject_groups = list(unique_subject_elective(elective_subject_groups))
        ElectiveStudentSubject.objects.bulk_create(
            [
                ElectiveStudentSubject(student=instance, **elective_data)
                for elective_data in elective_subject_groups
            ],
            ignore_conflicts=True,
        )
