from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('company', views.CompanyListRetrieveApiView)
router.register('news', views.NewsListRetrieveApiView)
router.register('technical-user', views.TechnicalUserListRetrieveApiView)
router.register('technical', views.TechnicalListRetrieveApiView)
router.register('webinar', views.WebinarListRetrieveApiView)

urlpatterns = [
    path('', include(router.urls)),
]
