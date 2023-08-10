from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from django.contrib.admin import AdminSite
# from .myadmin import MyAdmin as AdminSite

AdminSite.index_template = 'codelines-admin/index.html'
AdminSite.app_index_template = 'codelines-admin/app_index.html'

admin.site.site_header = "TakenExams Administration Centre"
admin.site.site_title = "TakenExams E-Reviewer Administration"

urlpatterns = [
    path(r'codelines/r/', include('reports.admin_reports.urls')),
    path(r'codelines/studio/', include('codelines.studio.urls')),
    path(r'', admin.site.urls),
]


