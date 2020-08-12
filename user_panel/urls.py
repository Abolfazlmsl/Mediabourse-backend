from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'user-panel'

router = routers.DefaultRouter()
router.register('watch-list', views.WatchListViewSet)
router.register('watch-list-item', views.WatchListItemViewSet)
router.register('basket', views.BasketViewSet)
router.register('user-technical', views.UserTechnicalViewSet)
router.register('user-comment', views.UserCommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('info/', views.UserInfoView.as_view(), name='user-info'),
    path('signup/', views.SignUpAPIView.as_view(), name='user-signup'),
    path('verify-user/', views.UserPhoneRegisterAPIView.as_view(), name='verify-user'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]
