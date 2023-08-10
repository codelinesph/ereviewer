from django.urls import path, include
from django.conf.urls import url
from django.conf import settings

from .views import students as studentViews

app_name = 'acad'
urlpatterns = [
    path('',studentViews.index),
    path('course/<int:id>',studentViews.couseView, name='course'),
    path('subject/<int:id>',studentViews.subjectView, name='subject'),
    path('topic/<int:id>',studentViews.topicView, name='topic'),
    path('exam/<int:id>',studentViews.examView.as_view(), name='exam'),
    path('exam/<int:id>/<action>',studentViews.examView.as_view()),
    path('lesson/<int:id>',studentViews.lessonView.as_view(), name='lesson'),
]