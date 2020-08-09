from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('company', views.CompanyListRetrieveApiView)

urlpatterns = [
    path('', include(router.urls)),
]
