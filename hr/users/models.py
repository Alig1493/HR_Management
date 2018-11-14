
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _

from hr.users.config import Config, Status
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.
    Email and password are required. Other fields are optional.
    A more descriptive tutorial can be found here
    http://www.caktusgroup.com/blog/2013/08/07/migrating-custom-user-model-django/
    """
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    name = models.CharField(_('Name'), max_length=255, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    role = models.IntegerField(choices=Config.CHOICES, null=True, blank=True)
    status = models.IntegerField(choices=Status.CHOICES, default=Status.OPEN)
    manager_approved = models.BooleanField(default=False)
    hr_reviewed_by = models.ForeignKey("self", null=True, blank=True,
                                       on_delete=models.SET_NULL, related_name="hr")
    manager_approved_by = models.ForeignKey("self", null=True, blank=True,
                                            on_delete=models.SET_NULL, related_name="manager")
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as active. '
                                                'Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s' % self.name
        return full_name.strip()

    def get_short_name(self):
        full_name = '%s' % self.name
        return full_name.strip()


class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewed_by")
    reviewed_by_role = models.IntegerField(choices=Config.CHOICES, null=True, blank=True)
    reviewed_on = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewed_on")
    reviewed_on_role = models.IntegerField(choices=Config.CHOICES, null=True, blank=True)
    review_type = models.IntegerField(choices=Config.CHOICES, null=True, blank=True)
    changed_from = models.CharField(max_length=50)
    changed_to = models.CharField(max_length=50)
