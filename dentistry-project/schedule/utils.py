from .models import BaseSchedule, DoctorSchedule
from django.core.exceptions import ValidationError


def compare_base_schedule_to_doctors(self: BaseSchedule):
    doctors_too_early = DoctorSchedule.objects.filter(
        weekday=self.weekday, start_time__lt=self.start_time, is_working=True)
    if doctors_too_early:
        self._message_doctors_too_early = (
            'Расписания докторов '
            f'{", ".join([str(doctor) for doctor in doctors_too_early])} '
            f'в {self.get_weekday_display().lower()} начинались слишком '
            'рано для только что внесенных изменений. Теперь их '
            f'расписания начинаются с {self.start_time.strftime("%H:00")}')
        doctors_too_early.update(start_time=self.start_time)
    doctors_too_late = DoctorSchedule.objects.filter(
        weekday=self.weekday, end_time__gt=self.end_time, is_working=True)
    if doctors_too_late:
        self._message_doctors_too_late = (
            'Расписания докторов '
            f'{", ".join([str(doctor) for doctor in doctors_too_late])} '
            f'в {self.get_weekday_display().lower()} заканчивались '
            'слишком поздно для только что внесенных изменений. Теперь их '
            'расписания заканчиваются в '
            f'{self.end_time.strftime("%H:00")}')
        doctors_too_late.update(end_time=self.end_time)


def check_if_docs_working(self: BaseSchedule):
    docs_sch_working = DoctorSchedule.objects.filter(weekday=self.weekday,
                                                     is_working=True)
    if docs_sch_working:
        self._message_doc_sch_working = (
            'В расписании докторов '
            f'{", ".join([str(doctor) for doctor in docs_sch_working])} '
            f'{self.get_weekday_display().lower()} был указан как рабочий '
            'день, но вы объявили его как не рабочий день у клиники. '
            'Теперь для всех докторов '
            f'{self.get_weekday_display().lower()} - нерабочий день')
        docs_sch_working.update(is_working=False)


def check_if_clinic_closed(self: BaseSchedule):
    if BaseSchedule.objects.get(weekday=self.weekday).is_open is False:
        raise ValidationError(
            'Доктор не может работать в день, когда не работает клиника'
        )


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
