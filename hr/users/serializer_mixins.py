from allauth.account.adapter import get_adapter
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from hr.users.config import Config


class ValidatorMixin:

    def validate_email(self, email):
        email = get_adapter().validate_unique_email(email)
        domain = email.split("@")[1]
        if domain not in Config.DOMAINS:
            raise serializers.ValidationError(_(f"{domain} is an invalid domain"))
        return email
