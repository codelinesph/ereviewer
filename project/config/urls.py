from django.urls import path, include
from django.conf.urls import url

from guest import views as guestViews


urlpatterns = [

    path('M5yX0hL-hsyVQrtMpYFnV-TJCe-FlIVx9z-VET37XFjf/', include('core.urls')),

    path('', guestViews.index.as_view(), name='main_home'),

    url(r'^_nested_admin/', include('nested_admin.urls')),
    url(r'u/', include('users.urls')),
    url(r't/', include('taken.urls')),
    url(r'^acad/', include('student.urls')),
    
    url(r'^account/', include('account.urls'))
]


