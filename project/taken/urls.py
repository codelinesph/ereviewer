from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers

from . import views

# router = routers.DefaultRouter()
# router.register(r'', ExamResultsViewSet)

app_name = 'taken'
urlpatterns = [
    path('', views.ExamsResultsView, name='index'),
    path('review/<int:id>', views.ExamsResultReview, name='review'),
    # path('', include(router.urls)),
]