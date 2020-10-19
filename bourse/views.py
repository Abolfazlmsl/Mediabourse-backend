import concurrent
import datetime
import logging
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
import pandas as pd
from django.conf import settings
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from mediabourse.settings import KAVENEGAR_APIKEY
from .serializers import \
    NewsListSerializer, \
    NewsRetrieveSerializer, \
    UserTechnicalSerializer, \
    TechnicalListSerializer, \
    TechnicalRetrieveSerializer, \
    WebinarSerializer, \
    FundamentalSerializer, \
    BazaarSerializer, \
    TutorialListSerializer, \
    TutorialRetrieveSerializer, \
    FileRepositorySerializer, \
    UserForgetSerializer, \
    WatchListSerializer, \
    WatchListItemSerializer, InstrumentSerializer, CommentSerializer, NotificationListSerializer, \
    NotificationDetailSerializer, TechnicalJSONUserSerializer, BugReportSerializer

from .models import Company, \
    News, \
    UserTechnical, \
    Technical, \
    Webinar, \
    HitCount, \
    Fundamental, \
    Bazaar, Tutorial, FileRepository, User, Meta, Index, \
    WatchList, WatchListItem, Instrumentsel, UserComment, Notification, TechnicalJSONUser

from . import models

from . import feed

from . import candle


def save_csv_candle(request):
    candle.feed_candle()
    return HttpResponse(("Text only, please."), content_type="text/plain")


def fill_data(request):
    # table = request.GET.get('table')
    # print(f"feed {table} table")
    #
    # if table == "index":
    #     feed.feed_index()
    # elif table == "exchange":
    #     feed.feed_exchange()
    # elif table == "market":
    #     feed.feed_market()
    # elif table == "board":
    #     feed.feed_board()
    # elif table == "instrumentgroup":
    #     feed.feed_instrumentgroup()
    # elif table == "instrumentexchangestate":
    #     feed.feed_instrumentexchangestate()
    # elif table == "assettype":
    #     feed.feed_assettype()
    # elif table == "assetstate":
    #     feed.feed_assetstate()
    # elif table == "fund":
    #     feed.feed_fund()
    # elif table == "category":
    #     feed.feed_category()
    # elif table == "asset":
    #     feed.feed_asset()
    # elif table == "company":
    #     feed.feed_company()
    # elif table == "instrument":
    #     # feed.feed_instrument()
    #     feed.feed_instrument_thread()
    # elif table == "feed_trademidday":
    #     feed.feed_trademidday("164")
    # elif table == "instrumentsel":
    #     feed.feed_instrumentsel()
    # elif table == "search_rahavard_instruments":
    #     feed.search_rahavard_instruments()

    feed.second_feed_tradedaily_thread(46978)
    # candle.feed_candle()

    return HttpResponse(f"Table processed", content_type="text/plain")


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

    # 9975, 15698

    # obj = models.Instrument.objects.filter(short_name__icontains="بین")
    # print(obj)
    # for itm in obj:
    #     print(itm.short_name
    #           , ' - ', itm.id
    #           , ' - ', itm.type
    #           , ' - ', itm.market
    #           , ' - ', itm.exchange_state
    #           , ' - ', itm.board)
    #
    # return JsonResponse({}, safe=False)


    instrument = request.GET.get('instrument')
    version = request.GET.get('version')
    print(instrument, version)

    # get index candles whiout thread
    # feed.feed_tradedaily(instrument)

    # get selected instrument
    obj = models.Instrumentsel.objects.get(id=instrument)

    if obj.index is not  None:
        # threading to get index candles
        feed.feed_indexdaily_thread(obj.index_id)
    else:
        # threading to get instrument candles
        feed.feed_tradedaily_thread(instrument)

    # get result candles
    trade = models.Tradedetail.objects.filter(instrument=instrument).order_by('date_time').values()

    return JsonResponse(list(trade), safe=False)


def chart_timeframes(request):
    # print("trade_daily")

    instrument = request.GET.get('instrument')
    last_date = request.GET.get('date')
    # print(instrument, last_date)



    symbol_timeframes = models.Chart.objects.filter(instrument=instrument)
    url = settings.MEDIA_ROOT.replace('\\', '/')
    res = []
    for itm in symbol_timeframes:
        url2 = url + itm.data.url
        url2 = url2.replace('/media//', '/') #diffrenet in server
        df = pd.read_csv(url2)  # read csv
        # json_data = df.to_json(r'./New_Products.json')

        if last_date is not None:
            mask = (df['<DTYYYYMMDD>'] > int(last_date))
            df = df.loc[mask]

        json_data = df.to_json(orient='values')

        # return JsonResponse(res, safe=False)
        res.append({
            'data': json_data,
            'timeframe': itm.timeFrame,
            'instrument': itm.instrument.id
        })

    return JsonResponse(res, safe=False)
    # get index candles without thread
    # feed.feed_tradedaily(instrument)

    # get selected instrument
    obj = models.Instrumentsel.objects.get(id=instrument)

    if obj.index is not None:
        # threading to get index candles
        feed.feed_indexdaily_thread(obj.index_id)
    else:
        # threading to get instrument candles
        feed.feed_tradedaily_thread(instrument)

    # get result candles
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
    permission_classes = [IsAuthenticated,] # [IsOwnerOrReadOnly]

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
-- BugReport class --
"""


class BugReportAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = BugReportSerializer
    permission_classes = []#[IsOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        # print('watchlist......', self.request.user)
        qs = models.BugReport.objects.all()
        query = self.request.GET.get("q")
        query_email = self.request.GET.get("email")
        if query is not None:
            qs = qs.filter(Q(text__icontains=query)).distinct()
        if query_email is not None:
            qs = qs.filter(Q(email=query_email)).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save()

    # post method for creat item
    def post(self, request, *args, **kwargs):
        print('create')
        return self.create(request, *args, **kwargs)


class BugReportRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = BugReportSerializer
    permission_classes = [ ]  # [IsOwnerOrReadOnly]

    def get_queryset(self):
        return models.BugReport.objects.all()


"""
-- User Json Technical class --
"""


class UserJsonTechnicalAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = TechnicalJSONUserSerializer
    permission_classes = [IsAuthenticated,]#[IsOwnerOrReadOnly]

    def get_queryset(self):
        # print('watchlist......', self.request.user)
        qs = TechnicalJSONUser.objects.filter(user=self.request.user)
        query = self.request.GET.get("q")
        query_instrument = self.request.GET.get("instrument")
        query_share = self.request.GET.get("share")
        if query is not None:
            qs = qs.filter(Q(name__icontains=query)).distinct()
        # fetch global share files
        if query_share is not None:
            qs = TechnicalJSONUser.objects.all()
            flag = True
            if query_share is "false":
                flag = False
            qs = qs.filter(Q(isShare=flag)).distinct()
        if query_instrument is not None:
            qs = qs.filter(Q(instrument=query_instrument)).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # post method for creat item
    def post(self, request, *args, **kwargs):
        print('create')
        return self.create(request, *args, **kwargs)


class UserJsonTechnicalRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = TechnicalJSONUserSerializer
    permission_classes = [IsAuthenticated, ]  # [IsOwnerOrReadOnly]

    def get_queryset(self):
        return TechnicalJSONUser.objects.filter(user=self.request.user)


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

    serializer_class = InstrumentSerializer
    queryset = Company.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['name']
    search_fields = ['name', 'short_name', 'short_english_name']
    ordering_fields = ['hit_count']
    ordering = ['-hit_count']

    def get_queryset(self):
        if self.action == 'retrieve':
            HitCount.objects.filter(date__lt=datetime.date.today()).delete()
            customer_ip = get_client_ip(self.request)
            try:
                current_instrument = Instrumentsel.objects.get(id=self.kwargs['pk'])
                try:
                    HitCount.objects.get(
                        ip=customer_ip,
                        instrument_id=self.kwargs['pk']
                    )
                except HitCount.DoesNotExist:
                    current_instrument.hit_count = current_instrument.hit_count + 1
                    current_instrument.save()
                    HitCount.objects.create(
                        ip=customer_ip,
                        company_id=self.kwargs['pk'],
                        date=datetime.date.today()
                    )
            except Instrumentsel.DoesNotExist:
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
    filterset_fields = ['category', 'is_important', 'instrument']
    search_fields = ['instrument__name', 'title', 'tag']
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
    filterset_fields = ['instrument']
    search_fields = ['instrument__name', 'title']
    ordering_fields = ['created_on']
    ordering = ['-created_on']

    def get_queryset(self):
        return self.queryset.filter(is_share=True)


class TechnicalListRetrieveApiView(viewsets.GenericViewSet,
                                   mixins.ListModelMixin,
                                   mixins.RetrieveModelMixin):
    """List and retrieve technical"""

    serializer_class = TechnicalListSerializer
    queryset = Technical.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['instrument']
    search_fields = ['instrument__name', 'title']
    ordering_fields = ['created_on', 'hit_count']
    ordering = ['-created_on']

    def get_queryset(self):
        queryset = self.queryset
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

        video = self.request.GET.get('video')
        if video == 'true':
            queryset = queryset.exclude(video__exact='')
        elif video == 'false':
            queryset = queryset.filter(video__exact='')

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TechnicalRetrieveSerializer
        return self.serializer_class


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
    search_fields = ['instrument__name', 'title']
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
    search_fields = ['instrument__name', 'title']
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
    search_fields = ['instrument__name', 'title']
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
    """List and retrieve tutorial"""

    serializer_class = TutorialListSerializer
    queryset = Tutorial.objects.filter(free=False)

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

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TutorialRetrieveSerializer
        return self.serializer_class


class FreeTutorialListRetrieveApiView(viewsets.GenericViewSet,
                                      mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin):
    """List and retrieve free tutorial"""

    serializer_class = TutorialListSerializer
    queryset = Tutorial.objects.filter(free=True)
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

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TutorialRetrieveSerializer
        return self.serializer_class


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
                      'message': 'مدیابورس\n' + 'رمزعبور جدید شما:' + password}
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


class UserCommentListApiView(generics.ListAPIView):
    """
        List user comment
    """
    serializer_class = CommentSerializer
    queryset = UserComment.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = [
        'technical',
        'fundamental',
        'company',
        'webinar',
        'news'
    ]
    ordering_fields = ['created_on', 'like']
    ordering = ['-created_on']


class InstrumentListRetrieveViewSet(viewsets.GenericViewSet,
                                    mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin):
    """
        List and retrieve instruments
    """

    serializer_class = InstrumentSerializer
    queryset = Instrumentsel.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['market', 'group']
    search_fields = ['name']
    ordering_fields = ['created_on', 'hit_count']


class NotificationListRetrieveViewSet(viewsets.GenericViewSet,
                                      mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin):
    """
        List and retrieve notification
    """
    serializer_class = NotificationListSerializer
    queryset = Notification.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['company']
    search_fields = ['title']
    ordering_fields = ['created_on']
    ordering = ['-created_on']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NotificationDetailSerializer
        return self.serializer_class
