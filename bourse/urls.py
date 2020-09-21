from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('company', views.CompanyListRetrieveApiView)
router.register('news', views.NewsListRetrieveApiView)
router.register('user-technical', views.UserTechnicalListRetrieveApiView)
router.register('technical', views.TechnicalListRetrieveApiView)
router.register('webinar', views.WebinarListRetrieveApiView)
router.register('fundamental', views.FundamentalListRetrieveApiView)
router.register('bazaar', views.BazaarListRetrieveApiView)
router.register('tutorial', views.TutorialListRetrieveApiView)
router.register('file-repository', views.FileRepositoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'forget-password/',
        views.ForgetPasswordAPIView.as_view(),
        name='forget-password'
    ),
    path('fillData/',  views.fill_data, name='fill-data'),
    path('api-test/',  views.test_data, name='test-data'),
]
