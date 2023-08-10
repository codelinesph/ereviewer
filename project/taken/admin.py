from django.contrib import admin
import nested_admin
from django.utils.safestring import mark_safe
from .models import *
# Register your models here.

class AttemptAnswerInline(nested_admin.NestedTabularInline):
    model = AttemptAnswer
    extra = 0

class AttemptQuestionInline(nested_admin.NestedTabularInline):
    inlines = [AttemptAnswerInline,]
    model = AttemptQuestion
    extra = 0

class AttemptExamAdmin(nested_admin.NestedModelAdmin):
    model = AttemptExam
    list_display = (
        'exam',
        'student',
        'item_count',
        'my_score'
    )

    list_filter = ('original_exam', 'topic_exam')
    search_fields = ('owner','original_exam', 'topic_exam')
    
    # change_list_template = "codelines-admin/change_list.html"

    inlines = [AttemptQuestionInline,]
    def exam(self,obj):
        if obj.original_exam:
            return obj.original_exam.name
        elif obj.course_exam:
            return str(obj.course_exam.name) + ' General Assessment'
        elif obj.subject_exam:
            return str(obj.subject_exam.name) + ' General Assessment'
        elif obj.topic_exam:
            return str(obj.topic_exam.name) + ' General Assessment'
    def student(self,obj):
        return mark_safe("<a href='/admin/auth/user/"+str(obj.owner.id)+"/change/'>"+obj.owner.username+"</a>")
    def item_count(self,obj):
        return obj.attemptquestion_set.count()

    student.allow_tags = True


admin.site.register(AttemptExam,AttemptExamAdmin)
# admin.site.register(AttemptQuestion)
# admin.site.register(AttemptAnswer)