from django.urls import path, include
from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from .views import api

app_name = "codelines_studio"
router = DefaultRouter()
router.register(r'exam', api.ExamViewset)
router.register(r'examdata', api.CompleteExamDataViewset)
router.register(r'question', api.QuestionViewset)
router.register(r'answer', api.AnswerViewset)

urlpatterns = [
    path('', include(router.urls)),
]