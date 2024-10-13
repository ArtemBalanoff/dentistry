import datetime as dt
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from dentistry.constants import NAME_MAX_LENGTH, PHONE_MAX_LENGTH
from django.db.models.signals import post_save
from django.dispatch import receiver
from .validators import phone_number_validator


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Номер телефона - обязательное поле.')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Суперпользователь должен иметь статус персонала')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Суперпользователь должен иметь статус суперпользователя')

        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField('Имя', max_length=NAME_MAX_LENGTH)
    last_name = models.CharField('Фамилия', max_length=NAME_MAX_LENGTH)
    surname = models.CharField('Отчество', max_length=NAME_MAX_LENGTH)
    phone_number = models.CharField(
        'Номер телефона', max_length=PHONE_MAX_LENGTH,
        unique=True, validators=(phone_number_validator,))
    birth_day = models.DateField('День Рождения', blank=True, null=True)
    USERNAME_FIELD = 'phone_number'
    objects = CustomUserManager()

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.surname}'

    @property
    def age(self):
        if not self.birth_day:
            return '-'
        stage = int((dt.date.today() - self.birth_day).total_seconds()
                    // (60 * 60 * 24 * 30 * 12))
        return f'{stage} лет (год(а))'

    @property
    def is_doctor(self):
        return hasattr(self, 'doctor_profile')

    @property
    def is_patient(self):
        return hasattr(self, 'patient_profile')


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


class StaffUser(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'админ'
        verbose_name_plural = 'Админы'

    def save(self, *args, **kwargs):
        self.is_staff = True
        super().save(*args, **kwargs)


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
    photo = models.ImageField('Фотография', upload_to='doctors/photos/',
                              blank=True, null=True)

    class Meta:
        verbose_name = 'профиль врача'
        verbose_name_plural = 'Врачи'

    def __str__(self):
        return str(self.user)

    @property
    def stage(self):
        return int((dt.date.today() - self.carier_start).total_seconds()
                   // (60 * 60 * 24 * 30 * 12))


class PatientProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='patient_profile')

    class Meta:
        verbose_name = 'профиль пациента'
        verbose_name_plural = 'Пациенты'

    @property
    def appointments_count(self):
        return self.appointments.count()

    def __str__(self):
        return str(self.user)


class Specialization(models.Model):
    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)

    class Meta:
        verbose_name = 'специализация врача'
        verbose_name_plural = 'Специализации врачей'

    def __str__(self):
        return self.name


@receiver(post_save, sender=DoctorProfile)
def auto_create_doctors_schedule(sender, instance, created, **kwargs):
    from schedule.models import DoctorSchedule
    if created:
        schedule = [DoctorSchedule(doctor=instance,
                                   weekday=weekday) for weekday in range(7)]
        DoctorSchedule.objects.bulk_create(schedule)
