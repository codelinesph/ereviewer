from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'user'
urlpatterns = [
    path(r'', views.UserLanding, name='landing'),

    path(r'profile', views.UserProfile, name='profile'),

    path(r'resetpassword/', views.UserPasswordReset.as_view(), name='reset_password'),

]