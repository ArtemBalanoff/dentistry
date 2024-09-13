from django.urls import path, include
from users.views import DoctorViewSet, PatientViewSet, SpecializationViewSet
from services.views import ServiceViewSet, OptionViewSet
from appointments.views import (
    avaliable_days, avaliable_timeslots, AppointmentViewSet)
from rest_framework import routers
from schedule.views import (
    BaseScheduleViewSet, DoctorScheduleViewSet, ExceptionCaseViewSet)
from djoser.urls import urlpatterns as djoser_urls
from djoser.urls.jwt import urlpatterns as jwt_urls

router_v1 = routers.SimpleRouter()
router_v1.register('doctors', DoctorViewSet)
router_v1.register('patients', PatientViewSet)
router_v1.register('specializations', SpecializationViewSet)
router_v1.register('services', ServiceViewSet)
router_v1.register('options', OptionViewSet)
router_v1.register('appointments', AppointmentViewSet)
router_v1.register('clinic-schedule', BaseScheduleViewSet)
router_v1.register('doctors-schedule', DoctorScheduleViewSet)
router_v1.register('exceptions', ExceptionCaseViewSet)

urls_v1 = []
urls_v1.extend(router_v1.urls)
# urls_v1.extend(djoser_urls)
# urls_v1.extend(jwt_urls)

urlpatterns = [
    path('v1/', include(urls_v1)),
    path('v1/get-available-days', avaliable_days),
    path('v1/get-available-timeslots', avaliable_timeslots),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
]
