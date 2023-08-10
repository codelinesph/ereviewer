from django.contrib import admin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin import AdminSite

from django.db.models import Max, Count

from django.contrib.auth.models import User

from content.models import exam
from content.models import topics
from users import models as subscriberModels

from taken import models as attemptModels
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        topic_id = request.GET.get('id')

        topic_info = get_object_or_404(topics.Topics.objects.all(),pk=topic_id)

        suscriptions_list = (subscriberModels.UserSubscriptions.objects.filter(course=topic_info.subject.course))

        exam_set_id_list = []

        for exam in topic_info.exam_set.all():
            exam_set_id_list.append(exam.id)

        student_attempts = (
            attemptModels.AttemptExam.objects
            .filter(original_exam__in = exam_set_id_list)
            .order_by('my_score')
            .distinct()
        )

        # note: this loops are only meant to be temporary, find a better alternative as this is highly inneficient!
        for attempt in student_attempts:
            for attempt_r in student_attempts:
                if(attempt_r != attempt):
                    if(attempt_r.owner == attempt.owner and attempt_r.original_exam == attempt.original_exam):
                        student_attempts = student_attempts.exclude(pk=attempt.pk)
        
        site_data = {
            "site_header" : admin.site.site_header,
            "site_title" : admin.site.site_title,
            "site_url" : admin.site.site_url,
            "topic_info" : topic_info,
            "suscriptions": suscriptions_list,
            "attempts" : student_attempts,
        }
        return render(request, 'admin_reports/index.html',site_data)
    else:
        return redirect('main_home')
