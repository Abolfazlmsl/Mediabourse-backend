from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import TutorialFreeFile, News, Article, NewsPodcast


class TutorialFreeFileSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = 'https'
    # 'always' 'hourly' 'daily' 'weekly' 'monthly' 'yearly' 'never'

    def items(self):
        return TutorialFreeFile.objects.all()

    def location(self, obj):
        return '/free-tutorials/' + str(obj.id)


class NewsSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.5
    protocol = 'https'
    # 'always' 'hourly' 'daily' 'weekly' 'monthly' 'yearly' 'never'

    def items(self):
        return News.objects.all()

    def location(self, obj):
        return '/news/' + str(obj.id)


class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    protocol = 'https'
    # 'always' 'hourly' 'daily' 'weekly' 'monthly' 'yearly' 'never'

    def items(self):
        return Article.objects.all()

    def location(self, obj):
        return '/news/' + str(obj.id)


class NewsPodcastSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = 'https'
    # 'always' 'hourly' 'daily' 'weekly' 'monthly' 'yearly' 'never'

    def items(self):
        return NewsPodcast.objects.all()

    def location(self, obj):
        return '/news/' + str(obj.id)


class StaticViewSitemap(Sitemap):

    def items(self):
        return [] # ['pannel:search-all', 'pannel:search-cve', 'pannel:search-cwe', 'pannel:search-capec']

    def location(self, obj):
        return reverse(obj)
