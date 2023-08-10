from django.urls import path, include
from django.conf.urls import url
from django.conf import settings

from student.views import acad as acadViews
from student.views import exam as examViews

app_name = 'acad'
urlpatterns = [
    path('',acadViews.index),
    path('course/exam/<int:id>',examViews.courseExamView.as_view(), name='course_exam'),
    path('course/exam/<int:id>/<action>',examViews.courseExamView.as_view()),
    path('course/<int:id>',acadViews.couseView, name='course'),
    
    path('subject/exam/<int:id>',examViews.subjectExamView.as_view(), name='subject_exam'),
    path('subject/exam/<int:id>/<action>',examViews.subjectExamView.as_view()),
    path('subject/<int:id>',acadViews.subjectView, name='subject'),

    path('topic/<int:id>',acadViews.topicView, name='topic'),
    path('exam/<int:id>',examViews.examView.as_view(), name='exam'),
    path('exam/<int:id>/<action>',examViews.examView.as_view()),
    path('lesson/<int:id>',acadViews.lessonView.as_view(), name='lesson'),
]