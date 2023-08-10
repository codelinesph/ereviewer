from django import forms

from django.forms import (
    ModelForm, PasswordInput, Textarea, TextInput
)

from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.utils.translation import gettext, gettext_lazy as _

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import *
from content.models import course

class PopulationCreateAdminForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class":"form-control rounded-0"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"class":"form-control rounded-0"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    class Meta:
        widgets = {
            'username': TextInput(attrs={
                'class':'form-control rounded-0'
            }),
        }

class PopulationChangeAdminForm(UserChangeForm):
    class Meta:
        widgets = {
            'password': PasswordInput(attrs={
                'class':'form-control rounded-0'
            }),
            'username': TextInput(attrs={
                'class':'form-control rounded-0'
            }),
        }

class SubscriptionAdminChangeAdmin(forms.ModelForm):
    owner = forms.ModelChoiceField(
        label=_("Subscriber:"),
        queryset=User.objects.all(),
        widget=forms.Select(attrs={
            "class":"form-control rounded-0 custom-select",
        })
    )
    course = forms.ModelChoiceField(
        label=_("Subscription Course:"),
        queryset=course.Course.objects.all(),
        widget=forms.Select(attrs={
            "class":"form-control rounded-0 custom-select",
        })
    )
    subscription_date = forms.CharField(
        label=_("Subscription Date Span:"),
        strip=False,
        widget=forms.TextInput(attrs={
            "class":"form-control rounded-0 date-range-picker",
            "id":"starting-date-selector"
        })
    )
    subscription_expiration_date = forms.CharField(
        label=_("Subscription Expiration Date:"),
        strip=False,
        widget=forms.TextInput(attrs={
            "class":"form-control rounded-0 date-range-picker d-none",
            "id":"ending-date-selector"
        })
    )
    class Meta:
        fields = ['course','owner','subscription_date','subscription_expiration_date','premium_member','active']
        model = UserSubscriptions