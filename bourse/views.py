from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework import filters

from .serializers import \
    CompanySerializer,\
    NewsListSerializer,\
    NewsRetrieveSerializer,\
    TechnicalUserSerializer

from .models import Company, News, TechnicalUser


class CompanyListRetrieveApiView(viewsets.GenericViewSet,
                                 mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin):
    """List and retrieve company"""

    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['type', 'bourse_type']
    search_fields = ['name', 'alias', 'symbol']
    ordering_fields = ['hit_count']
    ordering = ['-hit_count']


class NewsListRetrieveApiView(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.RetrieveModelMixin):
    """List and retrieve news"""

    serializer_class = NewsListSerializer
    queryset = News.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['category', 'is_important']
    search_fields = ['company__name', 'title', 'tag']
    ordering_fields = ['created_on', 'hit_count']
    ordering = ['-created_on']

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class
        else:
            return NewsRetrieveSerializer


class TechnicalUserListRetrieveApiView(viewsets.GenericViewSet,
                                       mixins.ListModelMixin,
                                       mixins.RetrieveModelMixin):
    """List and retrieve technical user"""

    serializer_class = TechnicalUserSerializer
    queryset = TechnicalUser.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['company']
    search_fields = ['company__name', 'title']
    ordering_fields = ['created_on']
    ordering = ['-created_on']

    def get_queryset(self):
        return self.queryset.filter(is_share=True)