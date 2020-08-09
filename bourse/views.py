from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework import filters

from .serializers import CompanySerializer
from .models import Company


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
    ordering = ['hit_count']
