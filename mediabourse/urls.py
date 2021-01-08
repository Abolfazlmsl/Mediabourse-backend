from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from bourse.sitemaps import StaticViewSitemap, TutorialFreeFileSitemap, NewsSitemap, ArticleSitemap, NewsPodcastSitemap

sitemaps = {'static': StaticViewSitemap, }
sitemaps_free_tutorials = {'TutorialFreeFileSitemap': TutorialFreeFileSitemap, }
sitemap_news = {'NewsSitemap': NewsSitemap, }
sitemap_articles = {'ArticleSitemap': ArticleSitemap, }
sitemap_news_podcast = {'NewsPodcastSitemap': NewsPodcastSitemap, }

from mediabourse import settings

import private_storage.urls

schema_view = get_swagger_view(title='MediaBourse API')


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    url(r'^sitemap_static.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^sitemap_free_tutorials.xml$', sitemap, {'sitemaps': sitemaps_free_tutorials}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^sitemap_news.xml$', sitemap, {'sitemaps': sitemap_news}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^sitemap_articles.xml$', sitemap, {'sitemaps': sitemap_articles}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^sitemap_podcast.xml$', sitemap, {'sitemaps': sitemap_news_podcast}, name='django.contrib.sitemaps.views.sitemap'),

    path('user-panel/', include('user_panel.urls')),
    path('bourse/', include('bourse.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('', schema_view),

    path('private-media/', include(private_storage.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
