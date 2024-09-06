from django.urls import path, include
# from doctors.views import DoctorViewSet, SpecializationViewSet
# from services.views import ServiceViewSet, OptionViewSet
from appointments.views import (
    avaliable_days, avaliable_timeslots, AppointmentViewSet)
from rest_framework import routers

router_v1 = routers.SimpleRouter()
# router_v1.register('doctors', DoctorViewSet)
# router_v1.register('specializations', SpecializationViewSet)
# router_v1.register('services', ServiceViewSet)
# router_v1.register('options', OptionViewSet)
router_v1.register('appointments', AppointmentViewSet)

urls_v1 = []
urls_v1.extend(router_v1.urls)

urlpatterns = [
    path('v1/', include(urls_v1)),
    path('v1/get-available-days', avaliable_days),
    path('v1/get-available-timeslots', avaliable_timeslots),
]
