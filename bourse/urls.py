from django.urls import path, include
from rest_framework.routers import DefaultRouter

from bourse import consumers
from . import views
from django.conf.urls import url

app_name = 'bourse'

router = DefaultRouter()
router.register('company', views.CompanyListRetrieveApiView)
router.register('news', views.NewsListRetrieveApiView)
router.register('user-technical', views.UserTechnicalListRetrieveApiView)
router.register('technical', views.TechnicalListRetrieveApiView)
router.register('webinar', views.WebinarListRetrieveApiView)
router.register('fundamental', views.FundamentalListRetrieveApiView)
router.register('bazaar', views.BazaarListRetrieveApiView)
router.register('tutorial', views.TutorialListRetrieveApiView)
router.register('article', views.ArticleListRetrieveApiView)
router.register('comment', views.UserCommentViewSet)
router.register('free-tutorial', views.FreeTutorialListRetrieveApiView)
router.register('instrument', views.InstrumentListRetrieveViewSet)
router.register('notification', views.NotificationListRetrieveViewSet)
router.register('news-podcast', views.NewsPodcastListRetrieveAPIView)


urlpatterns = [
    path('chat/', views.index, name='index'),
    # path('live/', consumers.NewsConsumer, name='index'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('', include(router.urls)),
    path(
        'forget-password/',
        views.ForgetPasswordAPIView.as_view(),
        name='forget-password'
    ),
    path('fillData/',  views.fill_data, name='fill-data'),
    path('candle/',  views.save_csv_candle, name='candle'),
    path('trade-midday/',  views.trade_midday_function, name='trade-midday'),
    path('api-test/',  views.test_data, name='test-data'),
    path('trade-daily/',  views.trade_daily, name='trade-daily'),
    path('chart_timeframes/',  views.chart_timeframes, name='chart-timeframes'),

    path('instrument/',  views.instrument_list, name='instrument-list'),
    path('watchlist2/',  views.watchlist, name='watchlist'),
    path('news-scraper/',  views.news_scraper_view, name='news-scraper'),
    path('list-tradeDetail/',  views.list_trade_detail, name='list-trade-detail'),
    path('instrument-info/',  views.instrument_info, name='instrument-info'),
    path('capitalChange/',  views.capital_change, name='capital-change'),
    path('AI/trade-detail/',  views.ai_trade_detail, name='ai-trade-detail'),
    path('AI/trade-detail-current/',  views.ai_trade_detail_current, name='ai-trade-detail-current'),
    path('instrument-info-single/',  views.get_Selected_instrument_info, name='get-Selected-instrument-info'),
    path('bazaar-info/',  views.bazaar_info, name='bazaar-info'),
    path('news-scraper/',  views.news_scraper_view, name='news-scraper'),
    url(r'^watchlist$', views.WatchlistAPIView.as_view(), name='watchlist-post-listcreate'),
    url(r'^watchlist/(?P<pk>\d+)/$', views.WatchlistRudView.as_view(), name='watchlist-post-rud'),
    url(r'^bug-report$', views.BugReportAPIView.as_view(), name='bugreport-post-listcreate'),
    url(r'^bug-report/(?P<pk>\d+)/$', views.BugReportRudView.as_view(), name='bugreport-post-rud'),
    url(r'^watchlist-item$', views.WatchlistItemAPIView.as_view(), name='watchlist-item-post-listcreate'),
    url(r'^watchlist-item/(?P<pk>\d+)/$', views.WatchlistItemRudView.as_view(), name='watchlist-item-post-rud'),
    url(r'^user-json-technical$', views.UserJsonTechnicalAPIView.as_view(), name='user-json-technical-post-listcreate'),
    url(r'^user-json-technical/(?P<pk>\d+)/$', views.UserJsonTechnicalRudView.as_view(), name='user-json-technical-post-rud'),
    url(r'^trade-details$', views.TradeDetailAPIView.as_view(), name='trade-detail-post-listcreate'),
    url(r'^current-trade-details$', views.CurrentTradeDetailAPIView.as_view()
        , name='current-trade-detail-post-listcreate'),
    url(r'^instrument-technical-info$', views.instrumentTechnicaInfoAPIView.as_view(),
        name='instrument-technical-info-post-listcreate'),
    url(r'^instrument-technical-info/(?P<pk>\d+)/$', views.instrumentTechnicaInfoRudView.as_view(),
        name='instrument-technical-info-post-rud'),
]
