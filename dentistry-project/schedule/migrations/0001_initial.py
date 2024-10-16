# Generated by Django 4.2.14 on 2024-10-13 09:52

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.PositiveSmallIntegerField(choices=[(0, 'Понедельник'), (1, 'Вторник'), (2, 'Среда'), (3, 'Четверг'), (4, 'Пятница'), (5, 'Суббота'), (6, 'Воскресенье')], unique=True, verbose_name='День недели')),
                ('start_time', models.TimeField(choices=[(datetime.time(0, 0), '0:00'), (datetime.time(1, 0), '1:00'), (datetime.time(2, 0), '2:00'), (datetime.time(3, 0), '3:00'), (datetime.time(4, 0), '4:00'), (datetime.time(5, 0), '5:00'), (datetime.time(6, 0), '6:00'), (datetime.time(7, 0), '7:00'), (datetime.time(8, 0), '8:00'), (datetime.time(9, 0), '9:00'), (datetime.time(10, 0), '10:00'), (datetime.time(11, 0), '11:00'), (datetime.time(12, 0), '12:00'), (datetime.time(13, 0), '13:00'), (datetime.time(14, 0), '14:00'), (datetime.time(15, 0), '15:00'), (datetime.time(16, 0), '16:00'), (datetime.time(17, 0), '17:00'), (datetime.time(18, 0), '18:00'), (datetime.time(19, 0), '19:00'), (datetime.time(20, 0), '20:00'), (datetime.time(21, 0), '21:00'), (datetime.time(22, 0), '22:00'), (datetime.time(23, 0), '23:00')], default=datetime.time(0, 0), verbose_name='Начало рабочего дня')),
                ('end_time', models.TimeField(choices=[(datetime.time(0, 0), '0:00'), (datetime.time(1, 0), '1:00'), (datetime.time(2, 0), '2:00'), (datetime.time(3, 0), '3:00'), (datetime.time(4, 0), '4:00'), (datetime.time(5, 0), '5:00'), (datetime.time(6, 0), '6:00'), (datetime.time(7, 0), '7:00'), (datetime.time(8, 0), '8:00'), (datetime.time(9, 0), '9:00'), (datetime.time(10, 0), '10:00'), (datetime.time(11, 0), '11:00'), (datetime.time(12, 0), '12:00'), (datetime.time(13, 0), '13:00'), (datetime.time(14, 0), '14:00'), (datetime.time(15, 0), '15:00'), (datetime.time(16, 0), '16:00'), (datetime.time(17, 0), '17:00'), (datetime.time(18, 0), '18:00'), (datetime.time(19, 0), '19:00'), (datetime.time(20, 0), '20:00'), (datetime.time(21, 0), '21:00'), (datetime.time(22, 0), '22:00'), (datetime.time(23, 0), '23:00')], default=datetime.time(23, 0), verbose_name='Конец рабочего дня')),
                ('is_open', models.BooleanField(default=True, verbose_name='Открыто')),
            ],
            options={
                'verbose_name': 'расписание дня клиники',
                'verbose_name_plural': 'Расписание клиники',
                'ordering': ('weekday',),
            },
        ),
        migrations.CreateModel(
            name='DoctorSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.PositiveBigIntegerField(choices=[(0, 'Понедельник'), (1, 'Вторник'), (2, 'Среда'), (3, 'Четверг'), (4, 'Пятница'), (5, 'Суббота'), (6, 'Воскресенье')], verbose_name='День недели')),
                ('start_time', models.TimeField(choices=[(datetime.time(0, 0), '0:00'), (datetime.time(1, 0), '1:00'), (datetime.time(2, 0), '2:00'), (datetime.time(3, 0), '3:00'), (datetime.time(4, 0), '4:00'), (datetime.time(5, 0), '5:00'), (datetime.time(6, 0), '6:00'), (datetime.time(7, 0), '7:00'), (datetime.time(8, 0), '8:00'), (datetime.time(9, 0), '9:00'), (datetime.time(10, 0), '10:00'), (datetime.time(11, 0), '11:00'), (datetime.time(12, 0), '12:00'), (datetime.time(13, 0), '13:00'), (datetime.time(14, 0), '14:00'), (datetime.time(15, 0), '15:00'), (datetime.time(16, 0), '16:00'), (datetime.time(17, 0), '17:00'), (datetime.time(18, 0), '18:00'), (datetime.time(19, 0), '19:00'), (datetime.time(20, 0), '20:00'), (datetime.time(21, 0), '21:00'), (datetime.time(22, 0), '22:00'), (datetime.time(23, 0), '23:00')], default=datetime.time(0, 0), verbose_name='Начало рабочего дня')),
                ('end_time', models.TimeField(choices=[(datetime.time(0, 0), '0:00'), (datetime.time(1, 0), '1:00'), (datetime.time(2, 0), '2:00'), (datetime.time(3, 0), '3:00'), (datetime.time(4, 0), '4:00'), (datetime.time(5, 0), '5:00'), (datetime.time(6, 0), '6:00'), (datetime.time(7, 0), '7:00'), (datetime.time(8, 0), '8:00'), (datetime.time(9, 0), '9:00'), (datetime.time(10, 0), '10:00'), (datetime.time(11, 0), '11:00'), (datetime.time(12, 0), '12:00'), (datetime.time(13, 0), '13:00'), (datetime.time(14, 0), '14:00'), (datetime.time(15, 0), '15:00'), (datetime.time(16, 0), '16:00'), (datetime.time(17, 0), '17:00'), (datetime.time(18, 0), '18:00'), (datetime.time(19, 0), '19:00'), (datetime.time(20, 0), '20:00'), (datetime.time(21, 0), '21:00'), (datetime.time(22, 0), '22:00'), (datetime.time(23, 0), '23:00')], default=datetime.time(23, 0), verbose_name='Конец рабочего дня')),
                ('is_working', models.BooleanField(default=False, verbose_name='Работает')),
            ],
            options={
                'verbose_name': 'расписание дня доктора',
                'verbose_name_plural': 'Расписание докторов',
                'ordering': ('doctor', 'weekday'),
            },
        ),
        migrations.CreateModel(
            name='ExceptionCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('reason', models.TextField(default='Не указано', max_length=60, verbose_name='Причина')),
            ],
            options={
                'verbose_name': 'исключение',
                'verbose_name_plural': 'Исключения',
                'ordering': ('date',),
            },
        ),
    ]
