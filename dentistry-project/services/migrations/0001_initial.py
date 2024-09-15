# Generated by Django 4.2.14 on 2024-09-15 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('price', models.IntegerField(verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'опция услуги',
                'verbose_name_plural': 'Опции услуги',
                'ordering': ('service', 'price'),
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('duration', models.PositiveSmallIntegerField(choices=[(30, '30 минут'), (60, '1 час'), (120, '2 часа')], verbose_name='Продолжительность (в мин.)')),
            ],
            options={
                'verbose_name': 'услуга',
                'verbose_name_plural': 'Услуги',
                'ordering': ('specialization',),
            },
        ),
    ]
