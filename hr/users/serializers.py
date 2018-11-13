from allauth.account.adapter import get_adapter
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer, ValidationError

from hr.users.config import Config, Status
from hr.users.serializer_mixins import ValidatorMixin

User = get_user_model()


class RegisterSerializer(ValidatorMixin, serializers.Serializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True, max_length=255)
    profile_image = serializers.ImageField(required=True)
    role = serializers.IntegerField(min_value=Config.HR, max_value=Config.REGULAR)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate_name(self, value):
        if not value:
            return serializers.ValidationError(_("Must include name"))
        return value

    def validate_profile_image(self, value):
        if not value:
            return serializers.ValidationError(_("Must include profile image"))
        return value

    def validate_role(self, value):
        if not value:
            return serializers.ValidationError(_("Must include role"))
        return value

    def validate(self, data):
        super().validate(attrs=data)

        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def save(self, request):
        password = self.validated_data.pop('password1', None)
        self.validated_data.pop('password2', None)
        user = User.objects.create(**self.validated_data)
        if user.role == Config.HR or user.role == Config.MANAGER:
            user.status = Status.HR_REVIEWED
            user.manager_approved = True
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def _validate_email(self, email, password):
        # Should return 404 if no user found with this email
        # This is intentional as per requirements and specification
        user = get_object_or_404(User, email__iexact=email)
        if user and user.check_password(password):
            return user

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = self._validate_email(email, password)
        else:
            msg = _('Must include "email" and "password".')
            raise ValidationError(msg)

        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise ValidationError(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise ValidationError(msg)

        # Everything passed. That means password is accepted. So return the user
        attrs['user'] = user
        return attrs


class UserDetailsSerializer(ValidatorMixin, ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'manager_approved',
                  'status', 'role', 'is_superuser',
                  'hr_reviewed_by', 'manager_approved_by',
                  'profile_image')
        read_only_fields = ('is_superuser', 'manager_approved', 'status',
                            'hr_reviewed_by', 'manager_approved_by')


class UserPublicSerializer(ModelSerializer):

    full_name = serializers.CharField(source='get_full_name')

    class Meta:
        model = User
        fields = ('id', 'full_name', 'email')


class HRApproveSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = ["name", "status"]


class ManagerApproveSerializer(HRApproveSerializer):

    class Meta:
        model = User
        fields = ["name", "status", "manager_approved"]
        read_only_fields = ["status"]
