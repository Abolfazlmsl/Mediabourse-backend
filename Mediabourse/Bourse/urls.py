from django.urls import path, include
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^register/$', UserCreate.as_view(), name='account-create'),
    url(r'^change-password/$', ChangePasswordView.as_view(), name='change-password'),

]
