from django.contrib.auth.views import PasswordResetForm
from django.contrib.auth.views import SetPasswordForm
from django.contrib.auth.models import User
from users.models import UserData, UserSubscriptions

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)

from django.utils.translation import gettext, gettext_lazy as _

from django import forms

from content.models.course import Course

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label=_("Choose Your Username"),
        strip=False,
        widget=forms.TextInput(attrs={"class":"form-control rounded-0"}),
        help_text="Username Must Be Unique",
    )

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class":"form-control rounded-0"}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label=_("Confirm Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class":"form-control rounded-0"}),
        help_text=_("Enter the same password as before, for verification."),
    )

    first_name = forms.CharField(
        label=_("First Name"),
        strip=False,
        widget=forms.TextInput(attrs={"class":"form-control rounded-0"}),
    )

    last_name = forms.CharField(
        label=_("Last Name"),
        strip=False,
        widget=forms.TextInput(attrs={"class":"form-control rounded-0"}),
    )

    email = forms.EmailField(
        label=_("Email Address"),
        widget=forms.EmailInput(attrs={"class":"form-control rounded-0"}),
    )

    curriculum = forms.ModelChoiceField(
        queryset = Course.objects.filter(in_public=True),
        empty_label="-------------",
        required = True,
        label=_("Choose Your Curriculum"),
        widget=forms.Select(attrs={"class":"form-control rounded-0 custom-select"})
    )

    address = forms.CharField(
        label=_("Address"),
        strip=False,
        widget=forms.TextInput(attrs={"class":"form-control rounded-0"}),
    )

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','is_active']