from appointments.views import (AppointmentViewSet, avaliable_days,
                                avaliable_timeslots)
from django.urls import include, path
from djoser.urls import urlpatterns as djoser_urls
from djoser.urls.jwt import urlpatterns as jwt_urls
from rest_framework import routers
from schedule.views import (BaseScheduleViewSet, DoctorScheduleViewSet,
                            ExceptionCaseViewSet)
from services.views import OptionViewSet, ServiceViewSet

from users.views import DoctorViewSet, PatientViewSet, SpecializationViewSet

router_v1 = routers.SimpleRouter()
router_v1.register('doctors', DoctorViewSet, basename='doctor')
router_v1.register('patients', PatientViewSet, basename='patient')
router_v1.register('specializations', SpecializationViewSet,
                   basename='specialization')
router_v1.register('services', ServiceViewSet, basename='service')
router_v1.register('options', OptionViewSet, basename='option')
router_v1.register('appointments', AppointmentViewSet, basename='appointment')
router_v1.register('clinic-schedule', BaseScheduleViewSet,
                   basename='clinic-schedule')
router_v1.register('doctors-schedule', DoctorScheduleViewSet,
                   basename='doctors-schedule')
router_v1.register('exceptions', ExceptionCaseViewSet, basename='exception')
auth_urls = [
    path('auth/', include(djoser_urls)),
    path('auth/', include(jwt_urls)),
]

urls_v1 = []
urls_v1.extend(router_v1.urls)
urls_v1.extend(auth_urls)

urlpatterns = [
    path('v1/', include(urls_v1)),
    path('v1/get-available-days', avaliable_days),
    path('v1/get-available-timeslots', avaliable_timeslots),
]
