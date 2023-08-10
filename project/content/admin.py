from django.contrib import admin
from django.urls import reverse
from django.forms import TextInput, Textarea
from django.db import models
from datetime import datetime
import nested_admin

from django.utils.safestring import mark_safe

from django.forms import *

from .models.course import *
from .models.exam import *
from .models.subject import *
from .models.answer import *
from .models.question import *
from .models.topics import *
from .models.lesson import *

from users.models import UserSubscriptions

from .forms.admin import *

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    model = Course
    form = CourseForm

    search_fields = ['name','description']

    add_form_template = "codelines-admin/change_form.html"
    change_form_template = "codelines-admin/change_form.html"
    change_list_template = "codelines-admin/change_list.html"
    
    list_display = (
        'name',
        'subjects',
        'active_subscriptions',
        'expired_subscriptions',
        'in_public',
    )
    def subjects(self, obj):
        return obj.subject_set.count()

    def active_subscriptions(self, obj):
        return UserSubscriptions.objects.filter(
            course=obj,
            subscription_date__lte=datetime.now(),
            subscription_expiration_date__gte=datetime.now(),
        ).count()

    def expired_subscriptions(self, obj):
        return UserSubscriptions.objects.filter(
            course=obj,
            subscription_expiration_date__lt=datetime.now(),
        ).count()
  
class TopicsInlineAdmin(admin.StackedInline):
    model = Topics

class SubjectAdmin(admin.ModelAdmin):
    model = Subject
    search_fields = ['name','description']

    add_form_template = "codelines-admin/change_form.html"
    change_form_template = "codelines-admin/change_form.html"
    change_list_template = "codelines-admin/change_list.html"

    # inlines = [TopicsInlineAdmin,]
    
    form = SubjectForm
    def topic_items(self, obj):
        return obj.topics_set.count()

    list_display = (
        'name',
        'topic_items',
    )

class ExamAdmin(admin.ModelAdmin):
    model = Exam
    search_fields = ['name','description','arrangement']

    def questions(self, obj):
        return obj.question_set.count() or 0

    list_display = (
        'name',
        'premium_content',
        'questions',
    )

    change_list_template = "codelines-admin/change_list.html"

    add_form_template = "codelines-admin/change_form.html"
    change_form_template = "creator-studio/editor.html"

    form = ExamForm

    # inlines = [QuestionInline,]
  
class TopicsAdmin(admin.ModelAdmin):
    search_fields = ['name','description','subject']
    model = Topics
    form = TopicsForm
    add_form_template = "codelines-admin/change_form.html"
    change_form_template = "codelines-admin/change_form.html"
    change_list_template = "codelines-admin/change_list.html"

    list_display = (
        'name',
        'exams',
        'lessons',
        'premium_content',
        'my_actions',
    )

    def exams(self, obj):
        return obj.exam_set.count()

    def lessons(self, obj):
        return obj.lesson_set.count()

    def my_actions(self, obj):
        return mark_safe(
            "<div class='btn-group'>"+
                "<a class='btn btn-sm btn-outline-primary rounded-0' href='"+reverse("admin_reports:index")+"?id="+str(obj.id)+"'>"+
                    '<i class="fas fa-users"></i> '+
                    'Student Reports'+
                "<a>"+
            "</div>"
        )

class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    form = LessonForm
    add_form_template = "codelines-admin/change_form.html"
    change_form_template = "codelines-admin/change_form.html"
    change_list_template = "codelines-admin/change_list.html"

    list_display = (
        'name',
        'topic',
        'premium_content',
    )

    def topic(self, obj):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return mark_safe('<a href="' + reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,)) + ">"+ obj.name +"</a>")
    
admin.site.register(Course,CourseAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Topics, TopicsAdmin)
admin.site.register(Lesson, LessonAdmin)


