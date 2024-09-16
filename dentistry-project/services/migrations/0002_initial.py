# Generated by Django 4.2.14 on 2024-09-16 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='specialization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='users.specialization', verbose_name='Специализация'),
        ),
        migrations.AddField(
            model_name='option',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='services.service', verbose_name='Услуга'),
        ),
    ]
