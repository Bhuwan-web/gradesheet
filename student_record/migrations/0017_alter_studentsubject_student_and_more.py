# Generated by Django 5.1 on 2024-09-07 12:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_record', '0016_alter_studentsubject_th'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsubject',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='student_record.student'),
        ),
        migrations.AddConstraint(
            model_name='studentsubject',
            constraint=models.UniqueConstraint(models.F('subject'), models.F('student'), name='unique_student_subject'),
        ),
    ]
