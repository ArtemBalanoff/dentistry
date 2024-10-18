# Generated by Django 4.2.14 on 2024-10-13 09:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appointments', '0001_initial'),
        ('users', '0001_initial'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timeslots', to='users.doctorprofile'),
        ),
        migrations.AddField(
            model_name='appointmentoption',
            name='appointment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_options', to='appointments.appointment'),
        ),
        migrations.AddField(
            model_name='appointmentoption',
            name='option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.option'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='users.doctorprofile', verbose_name='Доктор'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='options',
            field=models.ManyToManyField(related_name='appointments', through='appointments.AppointmentOption', to='services.option'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='users.patientprofile', verbose_name='Пациент'),
        ),
        migrations.AddConstraint(
            model_name='timeslot',
            constraint=models.UniqueConstraint(fields=('date', 'start_time', 'doctor'), name='datetime_unique'),
        ),
    ]
