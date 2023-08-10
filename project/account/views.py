from django.shortcuts import redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from datetime import datetime, timedelta
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse

from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

from users.models import UserData, UserSubscriptions
from content.models.course import Course

from .forms import *

class ForgotPasswordView(PasswordResetView):
    form_class = ForgotPasswordForm
    from_email = "accounts@takenexams.com"
    template_name = "forgot_password.html"
    pass

class ForgotPasswordDoneView(PasswordResetDoneView):
    template_name = "forgot_password_done.html"
    pass

class ForgotasswordConfirmView(PasswordResetConfirmView):
    form_class = ForgotasswordConfirmForm
    template_name = "forgot_password_confirm.html"
    pass

class ForgotasswordCompleteView(PasswordResetCompleteView):
    template_name = "forgot_password_complete.html"
    pass

class MemberLoginView(LoginView):
    http_method_names = ['post','options']
    def post(self, request):
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('user:landing')
            else:
                messages.error(request, 'Please Check your email address and activate your account', extra_tags='login')
        else:
            messages.error(request, 'Username and/or pasword is either unknown or incorrect', extra_tags='login')
        return redirect('main_home')
    pass

class MemberLogoutView(LogoutView):
    next_page = 'main_home'
    pass

class AccountActivationView(View):
    http_method_names = ['get','options']
    def get(self, request, uidb64=None, token=None):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64).decode())
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            
            subscriptions = UserSubscriptions.objects.get(owner=user)

            subscriptions.active = True
            subscriptions.subscription_date=datetime.now()
            subscriptions.subscription_expiration_date = datetime.now()+timedelta(days=30)
            
            subscriptions.save()
            user.save()

            login(request, user)
            return redirect('user:landing')
        else:
            return HttpResponse("Activation link has expired")