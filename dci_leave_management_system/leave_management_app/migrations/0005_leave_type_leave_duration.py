# Generated by Django 4.1.2 on 2022-12-10 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_management_app', '0004_remove_leave_type_leave_max_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave_type',
            name='leave_duration',
            field=models.CharField(default='30/36 days', max_length=30),
        ),
    ]
