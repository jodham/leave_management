# Generated by Django 4.1.2 on 2022-11-23 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leave_management_app', '0003_rename_leave_description_leave_type_leave_type_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leave_type',
            name='leave_max_duration',
        ),
        migrations.AlterField(
            model_name='leave_application',
            name='leave_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave_management_app.leave_type'),
        ),
        migrations.DeleteModel(
            name='Leave',
        ),
    ]
