import datetime
import secrets
import string
import base64
import requests
import json

from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from kavenegar import KavenegarAPI, APIException, HTTPException
from rest_framework import mixins, viewsets, generics, status
from rest_framework import filters
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from mediabourse.settings import KAVENEGAR_APIKEY
from .serializers import \
    CompanySerializer, \
    NewsListSerializer, \
    NewsRetrieveSerializer, \
    UserTechnicalSerializer, \
    TechnicalSerializer, \
    WebinarSerializer, \
    FundamentalSerializer, \
    BazaarSerializer, TutorialSerializer, FileRepositorySerializer, UserForgetSerializer, \
    WatchListSerializer, WatchListItemSerializer

from .models import Company, \
    News, \
    UserTechnical, \
    Technical, \
    Webinar, \
    HitCount, \
    Fundamental, \
    Bazaar, Tutorial, FileRepository, User, Meta, Index, \
    WatchList, WatchListItem

from . import models

from . import feed


def fill_data(request):
    print("data test")

    # feed.feed_index()
    # feed.feed_exchange()
    # feed.feed_market()
    # feed.feed_board()
    # feed.feed_instrumentgroup()
    # feed.feed_instrumentexchangestate()
    # feed.feed_assettype()
    # feed.feed_assetstate()
    # feed.feed_fund()
    # feed.feed_categorie()
    # feed.feed_asset()
    # feed.feed_instrument()
    feed.feed_instrumentsel()

    return HttpResponse(("Text only, please."), content_type="text/plain")


def test_data(request):
    print("tes test")

    url = request.GET.get('url')
    print(url)

    url = url.replace("@", "&")
    # url = 'https://v1.db.api.mabnadp.com/exchange/indexes?_sort=meta.version&meta.version=4736142543&meta.version_op=gt&_count=100&_skip=0'
    # if version is not None:
    #     url = url + '&_sort=meta.version&meta.version='+version+'&meta.version_op=gt'
    access_token = b'd19573a3602e9c3c320bd8b3b737f28f'
    header_value = base64.b64encode(access_token + b':')
    headers = {'Authorization': b'Basic ' + header_value}
    req = requests.get(url, headers=headers)
    data = req.json()
    # print(req)

    # return HttpResponse(("test only, please." ), content_type="text/plain")
    # return JsonResponse(data, safe=False)
    return HttpResponse(json.dumps(data, ensure_ascii=False),
             content_type="application/json")


def trade_daily(request):
    print("trade_daily")

    instrument = request.GET.get('instrument')
    version = request.GET.get('version')
    print(instrument, version)

    feed.feed_tradedaily(instrument)

    trade = models.Tradedetail.objects.filter(instrument=instrument).order_by('date_time').values()

    return JsonResponse(list(trade), safe=False)


def instrument_list(request):
    print("instrument_list")

    instrument = request.GET.get('instrument')
    version = request.GET.get('version')
    print(instrument, version)

    if instrument is not None:
        trade = models.Instrumentsel.objects.filter(short_name__icontains=instrument).values('id', 'name', 'short_name')
    else:
        trade = models.Instrumentsel.objects.all().values('id', 'name', 'short_name')

    return JsonResponse(list(trade), safe=False)


def watchlist(request):
    print("watchlist")
    print(request.user)

    return JsonResponse({'error': 'enter watchlist name'}, safe=False)
    watchlist = request.POST.get('watchlist')

    if request.method == 'POST':

        watchlist = request.POST.get('watchlist')
        if watchlist is not None:
            obj_watchlist = models.WatchList(user=request.user, name=watchlist)
            obj_watchlist.save()
            return JsonResponse(list(obj_watchlist), safe=False)
        else:
            return JsonResponse({'error':'enter watchlist name'}, safe=False)

    else:
        watchlist = request.GET.get('watchlist')
        print(watchlist)

        if watchlist is not None:
            obj_watchlist = models.WatchList.objects.filter(name__icontains=watchlist).values('id', 'name', 'user')
        else:
            obj_watchlist = models.WatchList.objects.all().values('id', 'name', 'user')

        return JsonResponse(list(obj_watchlist), safe=False)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


"""
-- Watchlist class --
"""


class WatchlistAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = WatchListSerializer
    permission_classes = [IsAuthenticated,]#[IsOwnerOrReadOnly]

    def get_queryset(self):
        # print('watchlist......', self.request.user)
        qs = WatchList.objects.filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(name__icontains=query)).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # post method for creat item
    def post(self, request, *args, **kwargs):
        print('create')
        return self.create(request, *args, **kwargs)


class WatchlistRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = WatchListSerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    def get_queryset(self):
        return WatchList.objects.all()


"""
-- Watchlist item class --
"""


class WatchlistItemAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = WatchListItemSerializer
    permission_classes = [IsAuthenticated,]#[IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = WatchListItem.objects.filter(watch_list__user=self.request.user)
        return qs

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    # post method for creat item
    def post(self, request, *args, **kwargs):
        print('create')
        return self.create(request, *args, **kwargs)


class WatchlistItemRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = WatchListItemSerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    def get_queryset(self):
        return WatchListItem.objects.all()


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

    def get_queryset(self):
        if self.action == 'retrieve':
            HitCount.objects.filter(date__lt=datetime.date.today()).delete()
            customer_ip = get_client_ip(self.request)
            try:
                current_company = Company.objects.get(id=self.kwargs['pk'])
                try:
                    HitCount.objects.get(
                        ip=customer_ip,
                        company_id=self.kwargs['pk']
                    )
                except HitCount.DoesNotExist:
                    current_company.hit_count = current_company.hit_count + 1
                    current_company.save()
                    HitCount.objects.create(
                        ip=customer_ip,
                        company_id=self.kwargs['pk'],
                        date=datetime.date.today()
                    )
            except Company.DoesNotExist:
                pass

        return self.queryset


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

    def get_queryset(self):
        if self.action == 'retrieve':
            HitCount.objects.filter(date__lt=datetime.date.today()).delete()
            customer_ip = get_client_ip(self.request)
            try:
                current_news = News.objects.get(id=self.kwargs['pk'])
                try:
                    HitCount.objects.get(
                        ip=customer_ip,
                        news_id=self.kwargs['pk']
                    )
                except HitCount.DoesNotExist:
                    current_news.hit_count = current_news.hit_count + 1
                    current_news.save()
                    HitCount.objects.create(
                        ip=customer_ip,
                        news_id=self.kwargs['pk'],
                        date=datetime.date.today()
                    )
            except News.DoesNotExist:
                pass

        return self.queryset


class UserTechnicalListRetrieveApiView(viewsets.GenericViewSet,
                                       mixins.ListModelMixin,
                                       mixins.RetrieveModelMixin):
    """List and retrieve technical user"""

    serializer_class = UserTechnicalSerializer
    queryset = UserTechnical.objects.all()
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


class TechnicalListRetrieveApiView(viewsets.GenericViewSet,
                                   mixins.ListModelMixin,
                                   mixins.RetrieveModelMixin):
    """List and retrieve technical"""

    serializer_class = TechnicalSerializer
    queryset = Technical.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['company__name', 'title']
    ordering_fields = ['created_on', 'hit_count']
    ordering = ['-created_on']

    def get_queryset(self):
        if self.action == 'retrieve':
            HitCount.objects.filter(date__lt=datetime.date.today()).delete()
            customer_ip = get_client_ip(self.request)
            try:
                current_technical = Technical.objects.get(id=self.kwargs['pk'])
                try:
                    HitCount.objects.get(
                        ip=customer_ip,
                        technical_id=self.kwargs['pk']
                    )
                except HitCount.DoesNotExist:
                    current_technical.hit_count = current_technical.hit_count + 1
                    current_technical.save()
                    HitCount.objects.create(
                        ip=customer_ip,
                        technical_id=self.kwargs['pk'],
                        date=datetime.date.today()
                    )
            except Technical.DoesNotExist:
                pass

        return self.queryset


class WebinarListRetrieveApiView(viewsets.GenericViewSet,
                                 mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin):
    """List and retrieve webinar"""

    serializer_class = WebinarSerializer
    queryset = Webinar.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['company__name', 'title']
    ordering_fields = ['created_on', 'hit_count']
    ordering = ['-created_on']

    def get_queryset(self):
        if self.action == 'retrieve':
            HitCount.objects.filter(date__lt=datetime.date.today()).delete()
            customer_ip = get_client_ip(self.request)
            try:
                current_webinar = Webinar.objects.get(id=self.kwargs['pk'])
                try:
                    HitCount.objects.get(
                        ip=customer_ip,
                        webinar_id=self.kwargs['pk']
                    )
                except HitCount.DoesNotExist:
                    current_webinar.hit_count = current_webinar.hit_count + 1
                    current_webinar.save()
                    HitCount.objects.create(
                        ip=customer_ip,
                        webinar_id=self.kwargs['pk'],
                        date=datetime.date.today()
                    )
            except Webinar.DoesNotExist:
                pass

        return self.queryset


class FundamentalListRetrieveApiView(viewsets.GenericViewSet,
                                     mixins.ListModelMixin,
                                     mixins.RetrieveModelMixin):
    """List and retrieve fundamental"""

    serializer_class = FundamentalSerializer
    queryset = Fundamental.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['company__name', 'title']
    ordering_fields = ['created_on', 'hit_count']
    ordering = ['-created_on']

    def get_queryset(self):
        if self.action == 'retrieve':
            HitCount.objects.filter(date__lt=datetime.date.today()).delete()
            customer_ip = get_client_ip(self.request)
            try:
                current_fundamental = Fundamental.objects.get(id=self.kwargs['pk'])
                try:
                    HitCount.objects.get(
                        ip=customer_ip,
                        fundamental_id=self.kwargs['pk']
                    )
                except HitCount.DoesNotExist:
                    current_fundamental.hit_count = current_fundamental.hit_count + 1
                    current_fundamental.save()
                    HitCount.objects.create(
                        ip=customer_ip,
                        fundamental_id=self.kwargs['pk'],
                        date=datetime.date.today()
                    )
            except Fundamental.DoesNotExist:
                pass

        return self.queryset


class BazaarListRetrieveApiView(viewsets.GenericViewSet,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin):
    """List and retrieve bazaar"""

    serializer_class = BazaarSerializer
    queryset = Bazaar.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['company__name', 'title']
    ordering_fields = ['created_on', 'hit_count']
    ordering = ['-created_on']

    def get_queryset(self):
        if self.action == 'retrieve':
            HitCount.objects.filter(date__lt=datetime.date.today()).delete()
            customer_ip = get_client_ip(self.request)
            try:
                current_bazaar = Bazaar.objects.get(id=self.kwargs['pk'])
                try:
                    HitCount.objects.get(
                        ip=customer_ip,
                        bazaar_id=self.kwargs['pk']
                    )
                except HitCount.DoesNotExist:
                    current_bazaar.hit_count = current_bazaar.hit_count + 1
                    current_bazaar.save()
                    HitCount.objects.create(
                        ip=customer_ip,
                        bazaar_id=self.kwargs['pk'],
                        date=datetime.date.today()
                    )
            except Bazaar.DoesNotExist:
                pass

        return self.queryset


class TutorialListRetrieveApiView(viewsets.GenericViewSet,
                                  mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin):
    """List and retrieve bazaar"""

    serializer_class = TutorialSerializer
    queryset = Tutorial.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['sub_category']
    search_fields = ['sub_category__title', 'title']
    ordering_fields = ['created_on', 'hit_count']
    ordering = ['-created_on']

    def get_queryset(self):
        if self.action == 'retrieve':
            HitCount.objects.filter(date__lt=datetime.date.today()).delete()
            customer_ip = get_client_ip(self.request)
            try:
                current_tutorial = Tutorial.objects.get(id=self.kwargs['pk'])
                try:
                    HitCount.objects.get(
                        ip=customer_ip,
                        tutorial_id=self.kwargs['pk']
                    )
                except HitCount.DoesNotExist:
                    current_tutorial.hit_count = current_tutorial.hit_count + 1
                    current_tutorial.save()
                    HitCount.objects.create(
                        ip=customer_ip,
                        tutorial_id=self.kwargs['pk'],
                        date=datetime.date.today()
                    )
            except Tutorial.DoesNotExist:
                pass

        return self.queryset


class FileRepositoryViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin):
    serializer_class = FileRepositorySerializer
    queryset = FileRepository.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter
    ]
    filterset_fields = ['type']
    ordering_fields = ['created_on']
    ordering = ['-created_on']


class ForgetPasswordAPIView(generics.CreateAPIView):
    serializer_class = UserForgetSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        phone_number = self.request.POST.get('phone_number')
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(8))
        try:
            user = get_user_model().objects.get(phone_number=phone_number)
        except get_user_model().DoesNotExist:
            return Response(
                {
                    'message': 'شماره مورد نظر یافت نشد',
                },
                status=status.HTTP_404_NOT_FOUND
            )
        user.set_password(password)
        user.save()
        try:
            api = KavenegarAPI(KAVENEGAR_APIKEY)
            params = {'sender': '10008445', 'receptor': phone_number,
                      'message': 'کالا نگار\n' + 'رمزعبور جدید شما:' + password}
            api.sms_send(params)
            return Response(
                {
                    'message': 'رمز عبور به شماره موبایل وارد شده ارسال گردید',
                },
                status=status.HTTP_200_OK
            )
        except APIException:
            return Response(
                {
                    'error': 'ارسال رمز عبور با مشکل مواجه شده است',
                    'type': 'APIException'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except HTTPException:
            return Response(
                {
                    'error': 'ارسال رمز عبور با مشکل مواجه شده است',
                    'type': 'HTTPException'
                },
                status=status.HTTP_400_BAD_REQUEST
            )