from django.core.exceptions import ValidationError
from .models import BaseSchedule, DoctorSchedule


def start_end_time_validator(self: DoctorSchedule) -> None:
    if not self.start_time < self.end_time:
        raise ValidationError(
            'Время начала работы должно быть меньше времени конца работы')


def compare_doctors_schedule_to_base(self: DoctorSchedule) -> None:
    base_schedule = BaseSchedule.objects.get(
        weekday=self.weekday)
    if self.start_time < base_schedule.start_time:
        self.start_time = base_schedule.start_time
        self._message_too_early = (
            f'В {self.get_weekday_display().lower()} клиника работает '
            f'с {base_schedule.start_time.strftime("%H:00")}. Время '
            f'начала работы врача {self.doctor} изменено на '
            f'{base_schedule.start_time.strftime("%H:00")}.')
    if self.end_time > base_schedule.end_time:
        self.end_time = base_schedule.end_time
        self._message_too_late = (
            f'В {self.get_weekday_display().lower()} клиника работает '
            f'до {base_schedule.end_time.strftime("%H:00")}. Время '
            f'начала работы врача {self.doctor} изменено на '
            f'{base_schedule.end_time.strftime("%H:00")}.')
