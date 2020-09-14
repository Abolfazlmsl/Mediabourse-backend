import datetime
import secrets
import string

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from kavenegar import KavenegarAPI, APIException, HTTPException
from rest_framework import mixins, viewsets, generics, status
from rest_framework import filters
from rest_framework.response import Response

from mediabourse.settings import KAVENEGAR_APIKEY
from .serializers import \
    CompanySerializer, \
    NewsListSerializer, \
    NewsRetrieveSerializer, \
    UserTechnicalSerializer, \
    TechnicalSerializer, \
    WebinarSerializer, \
    FundamentalSerializer, \
    BazaarSerializer, TutorialSerializer, FileRepositorySerializer, UserForgetSerializer

from .models import Company, \
    News, \
    UserTechnical, \
    Technical, \
    Webinar, \
    HitCount, \
    Fundamental, \
    Bazaar, Tutorial, FileRepository, User


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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