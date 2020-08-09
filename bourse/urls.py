from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('company', views.CompanyListRetrieveApiView)
router.register('news', views.NewsListRetrieveApiView)
router.register('technical-user', views.TechnicalUserListRetrieveApiView)

urlpatterns = [
    path('', include(router.urls)),
]
