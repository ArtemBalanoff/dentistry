from datetime import date
from transliterate import translit
from django.db import models
from django.contrib.auth.models import AbstractUser
from dentistry.constants import NAME_MAX_LENGTH
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    # @property
    # def is_doctor(self):
    #     return hasattr(self, 'DoctorProfile')
    pass

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class DoctorUser(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'доктор'
        verbose_name_plural = 'Доктора'


class PatientUser(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'пациент'
        verbose_name_plural = 'Пациенты'


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    carier_start = models.DateField('Дата отсчета стажа')
    specialization = models.ForeignKey(
        'Specialization',
        on_delete=models.CASCADE,
        verbose_name='Специализация',
        related_name='doctors'
    )
    # slug = models.SlugField('Слаг', unique=True, blank=True, null=True)

    class Meta:
        verbose_name = 'профиль врача'
        verbose_name_plural = 'Врачи'

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         unique_slug = translit(value=f'{self.user.last_name}_{self.user.first_name}',
    #                                reversed=True)
    #         idx = 1
    #         while DoctorProfile.objects.filter(slug=unique_slug).exists():
    #             unique_slug = f'{unique_slug}_idx'
    #             idx += 1
    #         self.slug = unique_slug
    #     return super().save(*args, **kwargs)

    @property
    def stage(self):
        stage = int((date.today() - self.carier_start).total_seconds()
                    // (60 * 60 * 24 * 30 * 12))
        return f'{stage} лет (год)'


class PatientProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='patient_profile')
    age = models.SmallIntegerField('Возраст')

    class Meta:
        verbose_name = 'профиль пациента'
        verbose_name_plural = 'Пациенты'


class Specialization(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    # slug = models.SlugField('Слаг')

    class Meta:
        verbose_name = 'специализация врача'
        verbose_name_plural = 'Специализации врачей'

    def __str__(self):
        return self.name


@receiver(post_save, sender=DoctorProfile)
def auto_create_doctors_schedule(sender, instance, created, **kwargs):
    from schedule.models import DoctorSchedule
    if created:
        schedule = [DoctorSchedule(doctor=instance, weekday=weekday) for weekday in range(7)]
        DoctorSchedule.objects.bulk_create(schedule)
