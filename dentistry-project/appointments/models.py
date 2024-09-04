from django.db import models
from django.contrib.auth import get_user_model
from users.models import DoctorProfile
from services.models import Option

User = get_user_model()


class Appointment(models.Model):
    patient = models.ForeignKey(
        User,
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
    options = models.ManyToManyField(Option)

    class Meta:
        verbose_name = 'прием'
        verbose_name_plural = 'Приемы'

    @property
    def price(self):
        return sum(self.options.values('price'))


class TimeSlot(models.Model):
    date = models.DateField('День')
    start_time = models.TimeField('Время начала слота')
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE, verbose_name='timeslots'
    )
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE,
                               related_name='timeslots')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('date', 'start_time'),
                name='datetime_unique'
            )
        ]
