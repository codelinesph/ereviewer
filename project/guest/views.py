from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from datetime import datetime, timedelta
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse

from content.models.course import Course

from .forms import *

class index(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/u/')
        else:
            return render(request, 'index.html',{'signupform':SignUpForm()})

    def post(self, request):
        data = request.POST
        form = SignUpForm(request.POST)
        if(form.is_valid()):

            newuserinstance = form.save()
            user_data = UserData(owner=newuserinstance, address=form.cleaned_data['address'])
            initial_subscription = UserSubscriptions(
                owner=newuserinstance, 
                course=form.cleaned_data['curriculum'], 
                premium_member=False,
            )

            user_data.save()
            initial_subscription.save()

            user = newuserinstance
            text_content = 'Account Activation Email'
            subject = 'Email Activation'
            template_name = "emails/account/activation.html"
            from_email = "accounts@takenexams.com"
            recipients = [user.email]

            b64id = urlsafe_base64_encode(force_bytes(user.pk))

            # TEMPORARY WORKAROUND FOR INCOMPATIBLE DATATYPES
            if isinstance(b64id, str):
                validation = b64id
            else:
                validation = b64id.decode()

            kwargs = {
                "uidb64": validation,
                "token": default_token_generator.make_token(user)
            }
            activation_url = reverse("account_activation", kwargs=kwargs)

            activate_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), activation_url)

            context = {
                'user': user,
                'activate_url': activate_url
            }

            html_content = render_to_string(template_name, context)
            
            email = EmailMultiAlternatives(subject, text_content, from_email, recipients)
            email.attach_alternative(html_content, "text/html")
            email.send()
            return redirect('password_reset_done')
        else:
            return render(request, 'index.html',{'signupform':SignUpForm(request.POST)})
    pass



class GuestSignupView(View):
    http_method_names = ['post','options']
    def post(self, request):
        data = request.POST
        form = SignUpForm(request.POST)
        if(form.is_valid()):

            newuserinstance = form.save()
            user_data = UserData(
                owner=newuserinstance, 
                address=form.cleaned_data['address']
            )
            initial_subscription = UserSubscriptions(
                owner=newuserinstance, 
                course=form.cleaned_data['curriculum'], 
                premium_member=False,
            )

            user_data.save()

            user_data.set_password(form.cleaned_data['password1'])
            user_data.save()
            initial_subscription.save()

            user = newuserinstance
            text_content = 'Account Activation Email'
            subject = 'Email Activation'
            template_name = "emails/account/activation.html"
            from_email = "accounts@takenexams.com"
            recipients = [user.email]

            b64id = urlsafe_base64_encode(force_bytes(user.pk))

            # TEMPORARY WORKAROUND FOR INCOMPATIBLE DATATYPES
            if isinstance(b64id, str):
                validation = b64id
            else:
                validation = b64id.decode()

            kwargs = {
                "uidb64": validation,
                "token": default_token_generator.make_token(user)
            }
            activation_url = reverse("account_activation", kwargs=kwargs)

            activate_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), activation_url)

            context = {
                'user': user,
                'activate_url': activate_url
            }

            html_content = render_to_string(template_name, context)
            
            email = EmailMultiAlternatives(subject, text_content, from_email, recipients)
            email.attach_alternative(html_content, "text/html")
            email.send()
            return redirect('password_reset_done')
        else:
            return redirect('main_home')
    pass