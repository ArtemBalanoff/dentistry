# Generated by Django 4.2.14 on 2024-09-12 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'прием',
                'verbose_name_plural': 'Приемы',
            },
        ),
        migrations.CreateModel(
            name='AppointmentOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('start_time', models.TimeField(verbose_name='Время начала слота')),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timeslots', to='appointments.appointment')),
            ],
        ),
    ]
