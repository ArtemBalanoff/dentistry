from rest_framework import serializers

from .models import BaseSchedule, DoctorSchedule, ExceptionCase


class BaseScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseSchedule
        fields = '__all__'


class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = '__all__'


class ExceptionCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExceptionCase
        fields = '__all__'
