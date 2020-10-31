from random import randint

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from kavenegar import KavenegarAPI, APIException, HTTPException
from rest_framework import status, viewsets, mixins, filters
from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from mediabourse.settings import KAVENEGAR_APIKEY
from bourse.models import User, WatchList, WatchListItem, Basket, UserTechnical, UserComment, Note, Bookmark, Company, \
    Tutorial, RequestSymbol
from . import serializers
from .permissions import IsOwner, IsWatchListOwner


class UserInfoView(RetrieveUpdateAPIView):
    """Show detailed of user"""
    serializer_class = serializers.UserUpdateSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class SignUpAPIView(APIView):
    """
    User signup API
    """
    serializer_class = serializers.UserSignUpSerializer

    def post(self, request):
        serializer = serializers.UserSignUpSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = get_user_model().objects.get(phone_number=serializer.validated_data['phone_number'])
                if user.is_active:
                    return Response(
                        {
                            'message': 'کاربر با این اطلاعات وجود دارد. لطفا وارد شوید.',
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    print('11111111111111')
                    user.set_password(serializer.validated_data['password'])
                    user.generated_token = randint(100000, 999999)
                    user.save()
                    try:
                        api = KavenegarAPI(KAVENEGAR_APIKEY)
                        params = {'sender': '10006000660600', 'receptor': serializer.validated_data['phone_number'],
                                  'message': 'مدیابورس\n' + 'کد تایید:' + str(
                                      user.generated_token)}
                        response = api.sms_send(params)
                        return Response({"message": "کاربر با موفقیت ثبت نام شد."})

                    except APIException:
                        return Response(
                            {
                                'error': 'ارسال کد تایید با مشکل مواجه شده است',
                                'type': 'APIException'
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    except HTTPException:
                        return Response(
                            {
                                'error': 'ارسال کد تایید با مشکل مواجه شده است',
                                'type': 'HTTPException'
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )
            except get_user_model().DoesNotExist:
                print('222222222222')
                phone_number = serializer.validated_data['phone_number']
                user = User(
                    phone_number=phone_number,
                )
                password = serializer.validated_data['password']
                user.is_active = False
                user.set_password(password)
                user.generated_token = randint(100000, 999999)
                user.save()
                try:
                    api = KavenegarAPI(KAVENEGAR_APIKEY)
                    params = {'sender': '10006000660600', 'receptor': serializer.validated_data['phone_number'],
                              'message': 'مدیابورس\n' + 'کد تایید:' + str(user.generated_token)}
                    response = api.sms_send(params)
                    return Response({"message": "کاربر با موفقیت ثبت نام شد."})

                except APIException:
                    return Response(
                        {
                            'error': 'ارسال کد تایید با مشکل مواجه شده است',
                            'type': 'APIException'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except HTTPException:
                    return Response(
                        {
                            'error': 'ارسال کد تایید با مشکل مواجه شده است',
                            'type': 'HTTPException'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendSignUpTokenAPIView(APIView):
    """
    User verification via sms
    """

    def put(self, request):
        data = request.data
        user = get_object_or_404(get_user_model(), phone_number=data['phone_number'])
        print(user)
        if user:
            serializer = serializers.ResendSignUpTokenSerializer(user, data=data)
            if serializer.is_valid():
                serializer.validated_data['generated_token'] = randint(100000, 999999)
                user.save()
                try:
                    api = KavenegarAPI(KAVENEGAR_APIKEY)
                    params = {'sender': '10006000660600', 'receptor': serializer.validated_data['phone_number'],
                              'message': 'مدیابورس\n' + 'کد تایید:' + str(serializer.validated_data['generated_token'])}
                    response = api.sms_send(params)
                    return Response({"message": "کاربر با موفقیت ثبت نام شد."})

                except APIException:
                    return Response(
                        {
                            'error': 'ارسال کد تایید با مشکل مواجه شده است',
                            'type': 'APIException'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except HTTPException:
                    return Response(
                        {
                            'error': 'ارسال کد تایید با مشکل مواجه شده است',
                            'type': 'HTTPException'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            return Response({"user": "چنین کاربری وجود ندارد"})


class UserPhoneRegisterAPIView(APIView):
    """
    User verification via sms
    """

    def put(self, request):
        data = request.data
        user = get_object_or_404(get_user_model(), phone_number=data['phone_number'])
        print(user)
        if user:
            serializer = serializers.UserPhoneRegisterSerializer(user, data=data)
            if serializer.is_valid():
                if serializer.data['generated_token'] == int(data.get("generated_token")):
                    user.is_active = True
                    user.save()
                    return Response({"user": "verified successfully"})
                else:
                    return Response(
                        {
                            'error': 'The entered token is invalid'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = serializers.ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["رمز عبور فعلی نادرست میباشد!"]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListViewSet(viewsets.ModelViewSet):
    """
        User watchlist API
    """
    serializer_class = serializers.WatchListSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = WatchList.objects.all()

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.WatchListRetrieveSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WatchListItemViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.CreateModelMixin):
    """
        items of user watchlist API
    """
    serializer_class = serializers.WatchListItemCreateSerializer
    authentication_classes = (JWTAuthentication,)
    queryset = WatchList.objects.all()
    permission_classes = (IsAuthenticated, IsWatchListOwner)

    def get_queryset(self):
        return WatchListItem.objects.filter(watch_list__user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.WatchListItemListRetrieveSerializer
        else:
            return self.serializer_class


class BasketViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin):
    """
        User Basket API
    """
    serializer_class = serializers.BasketCreateSerializer
    authentication_classes = (JWTAuthentication,)
    queryset = Basket.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BasketSerializer
        else:
            return self.serializer_class


class UserTechnicalViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin):
    """
        user technical analytics API
    """
    serializer_class = serializers.UserTechnicalSerializer
    authentication_classes = (JWTAuthentication,)
    queryset = UserTechnical.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserTechnical.objects.filter(user=self.request.user)


class UserCommentViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin):
    """
        user comments API
    """
    serializer_class = serializers.UserCommentSerializer
    authentication_classes = (JWTAuthentication,)
    queryset = UserComment.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['comment_for']
    ordering_fields = ['created_on']

    def get_queryset(self):
        return UserComment.objects.filter(user=self.request.user)


class NoteViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin):
    """
        Note API
    """
    serializer_class = serializers.NoteSerializer
    authentication_classes = (JWTAuthentication,)
    queryset = Note.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    ordering_fields = ['created_on']

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


class BookmarkViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin):
    """
        user comments API
    """
    serializer_class = serializers.BookmarkSerializer
    authentication_classes = (JWTAuthentication,)
    queryset = Bookmark.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    ordering_fields = ['created_on']

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)


class InstrumentSearchListAPIView(ListAPIView):
    """
        Instrument search
    """
    serializer_class = serializers.InstrumentSearchSerializer
    authentication_classes = (JWTAuthentication,)
    queryset = Company.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_fields = ['name', 'id']
    search_fields = ['name']


class RequestSymbolViewSet(viewsets.GenericViewSet,
                           mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           mixins.DestroyModelMixin):
    """
        User Request Symbol API
    """
    serializer_class = serializers.RequestSymbolCreateSerializer
    authentication_classes = (JWTAuthentication,)
    queryset = RequestSymbol.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return RequestSymbol.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RequestSymbolSerializer
        else:
            return self.serializer_class
