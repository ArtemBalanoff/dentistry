from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import DoctorProfile, PatientProfile, Specialization
from .utils import get_profile_id_from_user

User = get_user_model()


class BaseUserSerializer(UserSerializer):
    id = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'phone_number', 'first_name',
                  'last_name', 'surname', 'email')

    def get_id(self, obj):
        return get_profile_id_from_user(obj)


class PublicDoctorUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ('first_name', 'last_name', 'surname')


class CustomUserCreateSerializer(UserCreateSerializer):
    id = serializers.SerializerMethodField()

    class Meta(UserCreateSerializer.Meta):
        pass

    def create(self, validated_data):
        user = super().create(validated_data)
        PatientProfile.objects.create(user=user)
        return user

    def get_id(self, obj):
        return get_profile_id_from_user(obj)


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ('id', 'specialization', 'stage')

    def to_representation(self, instance: DoctorProfile):
        repr_dict = super().to_representation(instance)
        base_user_dict = PublicDoctorUserSerializer(instance.user).data
        return {**repr_dict, **base_user_dict}


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ('user', 'appointments_count')

    def to_representation(self, instance: DoctorProfile):
        repr_dict = super().to_representation(instance)
        base_user_dict = BaseUserSerializer(instance.user).data
        return {**base_user_dict, **repr_dict}


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ('id', 'name')
