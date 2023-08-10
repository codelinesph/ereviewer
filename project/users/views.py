from django.shortcuts import redirect, render
from django.views import View
from datetime import datetime
from django.core import serializers
from django.core.paginator import Paginator

from django.conf import settings

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.db.models import Q

from content.models.course import Course
from content.models.subject import Subject
from .models import *

# Create your views here.

@login_required(login_url='/')
def UserLanding(request):
    subscriptions = UserSubscriptions.objects.filter(
        owner=request.user.id, 
        subscription_date__lte=datetime.now(),
        subscription_expiration_date__gte=datetime.now(),
    )
    course_list = []
    for subscription in subscriptions:
        course_list.append(subscription.course_id)
    
    search = request.GET.get('q')
    

    subject_list = Subject.objects.filter(course_id__in=course_list)

    if search is not None:
        subject_list = subject_list.filter(Q(name__icontains=search))

    page = request.GET.get('p')

    if page is None:
        page = 1
    else:
        try:
            page = int(page)
        except ValueError:
            page = 1
    if page<0:
        page = 1        

    paginator = Paginator(subject_list, settings.DEFAULT_QUERY_LIMIT)

    subjects = paginator.get_page(page)

    data = {
        "my_data": request.user,
        "subscriptions": subscriptions,
        "subjects":subjects,
        "subscription_json":serializers.serialize("json", subscriptions),
        "pagination":{
            "limit":settings.DEFAULT_QUERY_LIMIT,
            "page":page,
            "prev":page-1,
            "next":page+1,
            "paginator":paginator,
        }
    }
    return render(request, 'landing.html', data)

@login_required(login_url='/')
def UserProfile(request):
    subscriptions = UserSubscriptions.objects.filter(
        owner=request.user.id, 
        subscription_date__lte=datetime.now(),
        subscription_expiration_date__gte=datetime.now(),
        )
    data = {
        "subscriptions": subscriptions,
        "profile": request.user,
        "subscription_json":serializers.serialize("json", subscriptions),
    }
    return render(request, 'profile.html', data)

class UserPasswordReset(LoginRequiredMixin, View):
    http_method_names = ['post','options']
    def post(self, request):
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        repeat_new_password = request.POST.get('repeat_new_password')

        next_r = request.GET.get('next')

        user = authenticate(
        username=request.user.username,
        password=old_password
        )
        if user is not None:
            if new_password == repeat_new_password:
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, 'Successfully Changed Password')
            else:
                messages.error(request, 'Passwords Does not Match')
        else:
            messages.error(request, 'Failed')
        
        return redirect(next_r)