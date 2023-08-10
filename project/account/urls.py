from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views
from guest import views as guestViews

urlpatterns = [
    url(r'^forgot-password/$', views.ForgotPasswordView.as_view(), name='password_reset'),
    url(r'^email/sent/$', views.ForgotPasswordDoneView.as_view(), name='password_reset_done'),
    url(r'^forgot-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.ForgotasswordConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^forgot-password/success/$', views.ForgotasswordCompleteView.as_view(), name='password_reset_complete'),
    url(r'^login/$', views.MemberLoginView.as_view(), name='login'),
    url(r'^signup/$', guestViews.GuestSignupView.as_view(), name='signup'),
    url(r'^logout/$', views.MemberLogoutView.as_view(), name='logout'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.AccountActivationView.as_view(), name='account_activation'),
]

admin.site.site_header = "TakenExams Administration Centre"
admin.site.site_title = "TakenExams E-Reviewer Administration"
