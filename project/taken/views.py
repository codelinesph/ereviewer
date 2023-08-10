from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from datetime import datetime
from .models import *
from .serializers import *
from users.models import *

from content.models import course


@login_required(login_url='/')
def ExamsResultsView(request):
    http_method_names = ['get','options']
    queryset = AttemptExam.objects.filter(owner=request.user).order_by('-attempted_at')
    subscriptions = UserSubscriptions.objects.filter(
        owner=request.user.id, 
        subscription_date__lte=datetime.now(),
        subscription_expiration_date__gte=datetime.now(),
    )
    data = {
        "subscriptions": subscriptions,
        "results" : queryset
    }
    return render(request,"results.html", data)

@login_required(login_url='/')
def ExamsResultReview(request,id):
    http_method_names = ['get','options']
    queryset = AttemptExam.objects.filter(owner=request.user)
    attempt_data = get_object_or_404(queryset,id=id)
    subscriptions = UserSubscriptions.objects.filter(
        owner=request.user.id, 
        subscription_date__lte=datetime.now(),
        subscription_expiration_date__gte=datetime.now(),
    )

    data = {
        "subscriptions": subscriptions,
        "exam_data" : attempt_data,
    }
    return render(request,"review.html", data)
