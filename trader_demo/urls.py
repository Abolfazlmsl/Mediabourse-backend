from django.urls import path, include
from django.conf.urls import url
from .views import *
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'trader_demo'

# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register('company', views.CompanyCreate)
router.register('category', views.CategoryCreate)
router.register('watcher', views.WatcherCreate)
router.register('stocks', views.StockCreate)
router.register('order', views.Ordering)
router.register('cart', views.ManageCart)


urlpatterns = [
    url(r'^register/$', UserCreate.as_view(), name='account-create'),
    url(r'^change-password/$', ChangePasswordView.as_view(), name='change-password'),
    url('', include(router.urls)),
]
