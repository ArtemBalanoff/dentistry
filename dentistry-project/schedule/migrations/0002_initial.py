# Generated by Django 4.2.14 on 2024-10-13 09:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schedule', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exceptioncase',
            name='doctor',
            field=models.ForeignKey(blank=True, help_text='Оставьте поле пустым, если исключение для всей клиники', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exception_cases', to='users.doctorprofile', verbose_name='Доктор'),
        ),
        migrations.AddField(
            model_name='doctorschedule',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='users.doctorprofile', verbose_name='Доктор'),
        ),
        migrations.AddConstraint(
            model_name='doctorschedule',
            constraint=models.UniqueConstraint(fields=('weekday', 'doctor'), name='weekday_doctor_unique'),
        ),
    ]
