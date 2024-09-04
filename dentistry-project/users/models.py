from datetime import date
from transliterate import translit
from django.db import models
from django.contrib.auth.models import AbstractUser
from dentistry.constants import NAME_MAX_LENGTH


class CustomUser(AbstractUser):
    is_doctor = models.BooleanField('Доктор', default=False)

    # def save(self, *args, **kwargs):
    #     if self.is_doctor:
    #         if not hasattr(self, 'doctor_profile'):
    #             raise ValidationError('Доктор должен иметь связанный профиль доктора.')
    #         if hasattr(self, 'patient_profile'):
    #             raise ValidationError('Доктор не должен иметь связанный профиль пациента.')
    #     else:
    #         if hasattr(self, 'doctor_profile'):
    #             raise ValidationError('Пациент не должен иметь связанный профиль доктора.')
    #         if not hasattr(self, 'patient_profile'):
    #             raise ValidationError('Пациент должен иметь связанный профиль пациента.')

    #     try:
    #         super().save(*args, **kwargs)
    #     except ValidationError as e:
    #         # Превращаем ошибку валидации в исключение, чтобы админка показала сообщение
    #         raise ValidationError(e.message_dict)


class PatientProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='patient_profile')
    age = models.SmallIntegerField('Возраст')

    class Meta:
        verbose_name = 'профиль пациента'
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
    slug = models.SlugField('Слаг', unique=True, blank=True, null=True)

    class Meta:
        verbose_name = 'профиль врача'
        verbose_name_plural = 'Врачи'

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slug = translit(value=f'{self.user.last_name}_{self.user.first_name}',
                                   reversed=True)
            idx = 1
            while DoctorProfile.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{unique_slug}_idx'
                idx += 1
            self.slug = unique_slug
        return super().save(*args, **kwargs)

    @property
    def stage(self):
        stage = int((date.today() - self.carier_start).total_seconds()
                    // (60 * 60 * 24 * 30 * 12))
        return f'{stage} лет (год)'


class Specialization(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)

    class Meta:
        verbose_name = 'специализация врача'
        verbose_name_plural = 'Специализации врачей'

    def __str__(self):
        return self.name
