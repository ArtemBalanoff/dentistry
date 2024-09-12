from rest_framework import serializers
from .models import DoctorProfile, PatientProfile, Specialization
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer

User = get_user_model()


class BaseUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('phone_number', 'first_name', 'last_name',
                  'surname', 'email')


class CustomUserCreateSerializer(UserCreateSerializer):
    def create(self, validated_data):
        user = super().create(validated_data)
        PatientProfile.objects.create(user=user)
        return user


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'

    def to_representation(self, instance: DoctorProfile):
        repr_dict = super().to_representation(instance)
        repr_dict.pop('carier_start')
        repr_dict['stage'] = instance.stage
        base_user_dict = BaseUserSerializer(instance.user).data
        return {**repr_dict, **base_user_dict}


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = '__all__'

    def to_representation(self, instance: DoctorProfile):
        base_user_dict = BaseUserSerializer(instance.user).data
        base_user_dict['appointments_count'] = instance.appointments_count
        return base_user_dict


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'
