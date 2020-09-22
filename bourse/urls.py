from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf.urls import url


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
    path('trade-daily/',  views.trade_daily, name='trade-daily'),

    path('instrument/',  views.instrument_list, name='instrument-list'),
    path('watchlist2/',  views.watchlist, name='watchlist'),
    url(r'^watchlist$', views.WatchlistAPIView.as_view(), name='watchlist-post-listcreate'),
    url(r'^watchlist/(?P<pk>\d+)/$', views.WatchlistRudView.as_view(), name='watchlist-post-rud'),
    url(r'^watchlist-item$', views.WatchlistItemAPIView.as_view(), name='watchlist-item-post-listcreate'),
    url(r'^watchlist-item/(?P<pk>\d+)/$', views.WatchlistItemRudView.as_view(), name='watchlist-item-post-rud'),
]
