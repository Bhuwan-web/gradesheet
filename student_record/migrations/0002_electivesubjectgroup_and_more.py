# Generated by Django 5.1 on 2024-09-09 11:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_record', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectiveSubjectGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveConstraint(
            model_name='studentsubject',
            name='unique_student_subject',
        ),
        migrations.RenameField(
            model_name='classsubject',
            old_name='subject_id',
            new_name='subject',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='student_class',
            new_name='class_id',
        ),
        migrations.RemoveField(
            model_name='studentsubject',
            name='class_subject',
        ),
        migrations.AddField(
            model_name='studentsubject',
            name='subject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='student_record.subject'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subject',
            name='is_elective',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='subject_scores',
            field=models.ManyToManyField(through='student_record.StudentSubject', to='student_record.subject'),
        ),
        migrations.AddField(
            model_name='subject',
            name='elective_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student_record.electivesubjectgroup'),
        ),
    ]
