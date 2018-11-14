from allauth.account.adapter import get_adapter
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from hr.users.config import Config, ReviewType


class ValidatorMixin:

    def validate_email(self, email):
        email = get_adapter().validate_unique_email(email)
        domain = email.split("@")[1]
        if domain not in Config.DOMAINS:
            raise serializers.ValidationError(_(f"{domain} is an invalid domain"))
        return email


class LogMixins:

    def _get_user(self):
        return self.context["request"].user

    def _get_review_type(self, instance, validated_data):
        if validated_data.get("status"):
            return ReviewType.HR_REVIEW
        return ReviewType.MANAGER_APPROVAL

    def _get_review_change(self, review_type, instance, validated_data):
        if review_type == ReviewType.HR_REVIEW:
            return instance.status, validated_data["status"]
        return instance.manager_approved, validated_data["manager_approved"]
