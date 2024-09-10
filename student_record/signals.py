from django.db.models.signals import pre_save
from django.dispatch import receiver
from student_record.models.electives import ElectiveClass, ElectiveSubject


@receiver(pre_save, sender=ElectiveSubject)
def elective_subject_save(sender, instance: ElectiveSubject, **kwargs):
    classes = instance.subject.classes.all()
    ElectiveClass.objects.bulk_create(
        [
            ElectiveClass(elective_group=instance.elective_group, class_id=class_id)
            for class_id in classes
        ]
    )
