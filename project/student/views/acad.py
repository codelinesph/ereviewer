import io
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.views import View

from django.conf import settings

from rest_framework.parsers import JSONParser


from student import serializers as contentSerializers
from content import models as contentModels 
from users import models as userModels

from taken import serializers as takenSerializers
from users.models import *

from content.methods import takeexam

from django.db.models import Q

# Create your views here.

@login_required(login_url='main_home')
def index(request):
    return redirect("/u/")

@login_required(login_url='main_home')
def couseView(request,id):

    subscriptions = userModels.UserSubscriptions.objects.filter(
        owner=request.user, 
        subscription_date__lte=datetime.now(),
        subscription_expiration_date__gte=datetime.now(),
    )
    info = get_object_or_404(subscriptions, course_id=id)

    if info is not None:
        data = {
            "subscriptions": subscriptions,
            "info":info,
            "navigation":{
                "course":info.id,
            }
        }
        return render(request,"acad/course.html", data)
    else:
        raise Http404()

@login_required(login_url='main_home')
def subjectView(request,id):
    subscriptions = userModels.UserSubscriptions.objects.filter(
        owner=request.user, 
        subscription_date__lte=datetime.now(),
        subscription_expiration_date__gte=datetime.now(),
    )
    subscriptions_pks = []
  
    for subscription in subscriptions:
        subscriptions_pks.append(subscription.course_id)
    
    qset = contentModels.subject.Subject.objects.filter(course_id__in=subscriptions_pks)

    info = get_object_or_404(qset, id=id)

    course_info = subscriptions.get(course_id=info.course_id)

    if info is not None:
        data = {
            "info":info,
            "subscriptions":subscriptions,
            "navigation":{
                "subject":info.id,
                "course":info.course.id,
            },
            "course_info":course_info
        }
        return render(request,"acad/subject.html", data)
    else:
        raise Http404() 

@login_required(login_url='main_home')
def topicView(request,id):
    subscriptions = userModels.UserSubscriptions.objects.filter(
        owner=request.user, 
        subscription_date__lte=datetime.now(),
        subscription_expiration_date__gte=datetime.now(),
    )

    qset = contentModels.topics.Topics.objects.all()
    info = get_object_or_404(qset, pk=id)

    course_info = subscriptions.get(course_id=info.subject.course.id)

    arrangement_position = 0
    if(info.arrangement is not None):
        arrangement_position = info.arrangement

    nxt = qset.filter(
        Q(pk__gt = info.pk) | Q(arrangement__gt = arrangement_position),
        subject = info.subject.pk
    ).order_by('pk','arrangement').first()

    prev = qset.filter(
        Q(pk__lt = info.pk) | Q(arrangement__lt = arrangement_position),
        subject = info.subject.pk
    ).order_by('pk','arrangement').first()

    data = {
        "info":info,
        "subscriptions":subscriptions,
        "course_info":course_info,
        "next":nxt,
        "previous":prev,
        "navigation":{
            "topic":info.id,
            "subject":info.subject.id,
            "course":info.subject.course.id,
        }
    }
    return render(request,"acad/topic.html", data)


class lessonView(LoginRequiredMixin, View):
    http_method_names = ['options','get']
    def get(self, request, id):
        subscriptions = UserSubscriptions.objects.filter(
            owner=request.user, 
            subscription_date__lte=datetime.now(),
            subscription_expiration_date__gte=datetime.now(),
        )
        if(subscriptions is not None):
            qset = contentModels.lesson.Lesson.objects.all()
            info = get_object_or_404(qset, pk=id)

            arrangement_position = 0
            if(info.arrangement is not None):
                arrangement_position = info.arrangement

            nxt = qset.filter(
                Q(pk__gt = info.pk) | Q(arrangement__gt = arrangement_position),
                topic = info.topic.pk
            ).order_by('pk','arrangement').first()

            prev = qset.filter(
                Q(pk__lt = info.pk) | Q(arrangement__lt = arrangement_position),
                topic = info.topic.pk
            ).order_by('pk','arrangement').first()
            
            course_info = subscriptions.get(course_id=info.topic.subject.course.id)
            data = {
                "info":info,
                "subscriptions":subscriptions,
                "course_info":course_info,
                "next":nxt,
                "previous":prev,
                "navigation":{
                    "lesson":info.id,
                    "topic":info.topic.id,
                    "subject":info.topic.subject.id,
                    "course":info.topic.subject.course.id,
                }
            }
            return render(request, 'acad/lesson.html', data)
        else:
            raise Http404()
