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
router.register('note', views.NoteViewSet)
router.register('bookmark', views.BookmarkViewSet)
router.register('request-symbol', views.RequestSymbolViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('info/', views.UserInfoView.as_view(), name='user-info'),
    path('signup/', views.SignUpAPIView.as_view(), name='user-signup'),
    path('resend/', views.ResendSignUpTokenAPIView.as_view(), name='resend-token'),
    path('verify-user/', views.UserPhoneRegisterAPIView.as_view(), name='verify-user'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('instrument/', views.InstrumentSearchListAPIView.as_view(), name='instrument-search'),
    path('set-info/', views.SetInfoAPIView.as_view(), name='set-info')
]
