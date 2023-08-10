from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views as adminReportsView

app_name = "admin_reports"
urlpatterns = [
    path(r'', adminReportsView.index, name="index"),
]