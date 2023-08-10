from django.contrib.auth.views import PasswordResetForm
from django.contrib.auth.views import SetPasswordForm
from django.contrib.auth.models import User
from users.models import UserData, UserSubscriptions

from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)

from django.utils.translation import gettext, gettext_lazy as _

from django import forms

from content.models.course import Course

class ForgotPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control rounded-0'


class ForgotasswordConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(ForgotasswordConfirmForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control rounded-0'
