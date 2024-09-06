# Generated by Django 5.1 on 2024-09-06 06:56

from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("student_record", "0009_add_marks_table"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subject",
            name="practical_marks",
        ),
        migrations.RemoveField(
            model_name="subject",
            name="theory_marks",
        ),
        migrations.AddField(
            model_name="subject",
            name="marks",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="student_record.marks",
            ),
            preserve_default=False,
        ),
    ]
