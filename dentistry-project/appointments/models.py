from django.db import models
from users.models import DoctorProfile, PatientProfile
from services.models import Option


class Appointment(models.Model):
    date = models.DateField('Дата')
    patient = models.ForeignKey(
        PatientProfile,
        verbose_name='Пациент',
        related_name='appointments',
        on_delete=models.CASCADE
    )
    doctor = models.ForeignKey(
        DoctorProfile,
        verbose_name='Доктор',
        related_name='appointments',
        on_delete=models.CASCADE
    )
    options = models.ManyToManyField(
        Option, through='AppointmentOption', related_name='appointments')

    class Meta:
        verbose_name = 'прием'
        verbose_name_plural = 'Приемы'

    @property
    def price(self):
        return sum(self.options.values_list('price', flat=True))

    @property
    def services(self):
        return [option.service for option in self.options.all()]

    @property
    def min_price(self):
        return sum([service.min_price for service in self.services])

    @property
    def max_price(self):
        return sum([service.max_price for service in self.services])


class AppointmentOption(models.Model):
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE,
        related_name='appointment_options')
    option = models.ForeignKey(
        Option, on_delete=models.CASCADE)


class TimeSlot(models.Model):
    date = models.DateField('Дата')
    start_time = models.TimeField('Время начала слота')
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, related_name='timeslots'
    )
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE,
                               related_name='timeslots')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('date', 'start_time', 'doctor'),
                name='datetime_unique'
            )
        ]
