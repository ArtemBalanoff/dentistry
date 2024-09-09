case "$OSTYPE" in
    msys*)    python=python ;;
    cygwin*)  python=python ;;
    *)        python=python3 ;;
esac

cd dentistry-project/
$python manage.py migrate
$python manage.py flush --no-input
echo "import datetime as dt; \
    from django.contrib.auth import get_user_model; User = get_user_model(); \
    from users.models import DoctorProfile, PatientProfile, Specialization; \
    from services.models import Service, Option; \
    from schedule.models import BaseSchedule, DoctorSchedule, ExceptionCase; \
    \
    day_0_sch = BaseSchedule.objects.create(weekday=(day_0 := (dt.date.today().weekday()) % 7), start_time=dt.time(hour=10), end_time=dt.time(hour=14)); \
    day_1_sch = BaseSchedule.objects.create(weekday=(day_1 := (dt.date.today().weekday() + 1) % 7), start_time=dt.time(hour=10), end_time=dt.time(hour=14)); \
    day_2_sch = BaseSchedule.objects.create(weekday=(day_2 := (dt.date.today().weekday() + 2) % 7), start_time=dt.time(hour=10), end_time=dt.time(hour=14)); \
    day_3_sch = BaseSchedule.objects.create(weekday=(day_3 := (dt.date.today().weekday() + 3) % 7), start_time=dt.time(hour=10), end_time=dt.time(hour=14)); \
    day_4_sch = BaseSchedule.objects.create(weekday=(day_4 := (dt.date.today().weekday() + 4) % 7), start_time=dt.time(hour=10), end_time=dt.time(hour=14)); \
    day_5_sch = BaseSchedule.objects.create(weekday=(day_5 := (dt.date.today().weekday() + 5) % 7), is_open=False); \
    day_6_sch = BaseSchedule.objects.create(weekday=(day_6 := (dt.date.today().weekday() + 6) % 7), is_open=False); \
    \
    spec_ter = Specialization.objects.create(name='Терапевт'); \
    spec_ort = Specialization.objects.create(name='Ортодонт'); \
    doc_ter_1 = User.objects.create(first_name='Иван', last_name='Будько', surname='Степанович', password='password', phone_number='+79781111113'); \
    doc_ter_2 = User.objects.create(first_name='Юрий', last_name='Ковалев', surname='Анатольевич', password='password', phone_number='+79781111114'); \
    doc_ter_1_profile = DoctorProfile.objects.create(user=doc_ter_1, carier_start=dt.date(year=2020, month=1, day=1), specialization=spec_ter); \
    doc_ter_2_profile = DoctorProfile.objects.create(user=doc_ter_2, carier_start=dt.date(year=2018, month=1, day=1), specialization=spec_ter); \
    \
    doc_ort_1 = User.objects.create(first_name='Дмитрий', last_name='Буханкин', surname='Александрович', password='password', phone_number='+79781111115'); \
    doc_ort_1_profile = DoctorProfile.objects.create(user=doc_ort_1, carier_start=dt.date(year=2016, month=1, day=1), specialization=spec_ort); \
    \
    day_0_doc_ter_1_sch = DoctorSchedule.objects.filter(doctor=doc_ter_1_profile, weekday=day_0).update(is_working=True, start_time=dt.time(hour=10), end_time=dt.time(hour=14)); \
    day_0_doc_ter_2_sch = DoctorSchedule.objects.filter(doctor=doc_ter_2_profile, weekday=day_0).update(is_working=True, start_time=dt.time(hour=12), end_time=dt.time(hour=14)); \
    \
    day_1_doc_ter_1_sch = DoctorSchedule.objects.filter(doctor=doc_ter_1_profile, weekday=day_1).update(is_working=True, start_time=dt.time(hour=10), end_time=dt.time(hour=14)); \
    day_1_doc_ter_2_sch = DoctorSchedule.objects.filter(doctor=doc_ter_2_profile, weekday=day_1).update(is_working=True, start_time=dt.time(hour=12), end_time=dt.time(hour=14)); \
    \
    day_2_doc_ter_1_sch = DoctorSchedule.objects.filter(doctor=doc_ter_1_profile, weekday=day_2).update(is_working=True, start_time=dt.time(hour=10), end_time=dt.time(hour=12)); \
    day_2_doc_ter_2_sch = DoctorSchedule.objects.filter(doctor=doc_ter_2_profile, weekday=day_2).update(is_working=True, start_time=dt.time(hour=11), end_time=dt.time(hour=12)); \
    \
    patient_1 = User.objects.create(first_name='Андрей', last_name='Крамер', surname='Игоревич', password='password', phone_number='+79781111111'); \
    patient_2 = User.objects.create(first_name='Саня', last_name='Бетон', surname='Арматурович', password='password', phone_number='+79781111112'); \
    patient_1_profile = PatientProfile.objects.create(user=patient_1); \
    patient_2_profile = PatientProfile.objects.create(user=patient_2); \
    \
    service_caries = Service.objects.create(name='Кариес', description='Лечение кариеса', duration=60, specialization=spec_ter); \
    caries_option_1 = Option.objects.create(name='Легкая степень', price=6000, service=service_caries); \
    caries_option_2 = Option.objects.create(name='Средняя степень', price=7500, service=service_caries); \
    caries_option_3 = Option.objects.create(name='Тяжелая степень', price=9000, service=service_caries); \
    service_nerve = Service.objects.create(name='Удаление нерва', description='Удаление нерва', duration=120, specialization=spec_ter); \
    nerve_option_1 = Option.objects.create(name='Легкая степень', price=12000, service=service_nerve); \
    nerve_option_2 = Option.objects.create(name='Средняя степень', price=14000, service=service_nerve); \
    nerve_option_3 = Option.objects.create(name='Тяжелая степень', price=16000, service=service_nerve); \
    service_consultation_ter = Service.objects.create(name='Консультация терапевта', description='Консультация терапевта', duration=30, specialization=spec_ter); \
    consultation_ter_option_1 = Option.objects.create(name='Базовая консультация', price=0, service=service_consultation_ter); \
    superuser = User.objects.create(phone_number='+79788806140'); superuser.is_superuser=True; superuser.is_staff=True; superuser.set_password('password'); superuser.save()" \
    | $python manage.py shell
echo "Setup done."