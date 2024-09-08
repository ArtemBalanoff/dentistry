case "$OSTYPE" in
    msys*)    python=python ;;
    cygwin*)  python=python ;;
    *)        python=python3 ;;
esac

source venv/bin/activate
cd dentistry-project/
$python manage.py migrate
$python manage.py flush --no-input
echo "import datetime as dt; \
    from django.contrib.auth import get_user_model; User = get_user_model(); \
    from users.models import DoctorProfile, PatientProfile, Specialization; \
    from services.models import Service, Option; \
    from schedule.models import BaseSchedule, DoctorSchedule, ExceptionCase; \
    \
    spec_ter = Specialization.objects.create(name='Терапевт'); \
    doc_ter_1 = User.objects.create(username='doc_ter_1', first_name='Иван', last_name='Будько', password='password'); \
    doc_ter_2 = User.objects.create(username='doc_ter_2', first_name='Юрий', last_name='Ковалев', password='password'); \
    doc_ter_1_profile = DoctorProfile.objects.create(user=doc_ter_1, carier_start=dt.date(year=2020, month=1, day=1), specialization=spec_ter); \
    doc_ter_2_profile = DoctorProfile.objects.create(user=doc_ter_2, carier_start=dt.date(year=2018, month=1, day=1), specialization=spec_ter); \
    \
    day_0_sch = BaseSchedule.objects.create(weekday=(day_0 := (dt.date.today().weekday()) % 7), start_time=dt.time(hour=10), end_time=dt.time(hour=14)); \
    day_1_sch = BaseSchedule.objects.create(weekday=(day_1 := (dt.date.today().weekday() + 1) % 7), start_time=dt.time(hour=10), end_time=dt.time(hour=14)); \
    day_2_sch = BaseSchedule.objects.create(weekday=(day_2 := (dt.date.today().weekday() + 2) % 7), start_time=dt.time(hour=10), end_time=dt.time(hour=12)); \
    day_3_sch = BaseSchedule.objects.create(weekday=(day_3 := (dt.date.today().weekday() + 3) % 7), is_open=False); \
    day_4_sch = BaseSchedule.objects.create(weekday=(day_4 := (dt.date.today().weekday() + 4) % 7), start_time=dt.time(hour=10), end_time=dt.time(hour=14)); \
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
    patient_1 = User.objects.create(username='patient_1', first_name='Андрей', last_name='Крамер', password='password'); \
    patient_2 = User.objects.create(username='patient_2', first_name='Саня', last_name='Бетон', password='password'); \
    patient_1_profile = PatientProfile.objects.create(user=patient_1, age=15); \
    patient_2_profile = PatientProfile.objects.create(user=patient_2, age=18); \
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
    superuser = User.objects.create(username='superuser'); superuser.is_superuser=True; superuser.is_staff=True; superuser.set_password('password'); superuser.save()" \
    | $python manage.py shell
echo "Setup done."