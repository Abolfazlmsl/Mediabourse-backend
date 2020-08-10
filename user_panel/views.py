from random import randint

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from kavenegar import KavenegarAPI, APIException, HTTPException
from rest_framework import status, viewsets, mixins
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
from bourse.models import User, WatchList, WatchListItem
from . import serializers
from .permissions import IsOwner, IsWatchListOwner


class UserInfoView(RetrieveUpdateAPIView):
    """Show detailed of user"""
    serializer_class = serializers.UserUpdateSerializer
    authentication_classes = (JWTAuthentication,)

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
            serializer.validated_data['generated_token'] = randint(100000, 999999)
            serializer.save()
            try:
                api = KavenegarAPI(KAVENEGAR_APIKEY)
                params = {'sender': '1000596446', 'receptor': serializer.validated_data['phone_number'],
                          'message': 'کالا نگار\n' + 'کد تایید:' + str(serializer.validated_data['generated_token'])}
                response = api.sms_send(params)
                return Response({"user": "signed up successfully",
                                 "generated token": serializer.data['generated_token']})

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


class UserPhoneRegisterAPIView(APIView):
    """
    User verification via sms
    """
    def put(self, request):
        data = request.data
        user = get_object_or_404(get_user_model(), phone_number=data['phone_number'])
        if user:
            serializer = serializers.UserPhoneRegisterSerializer(user, data=data)
            if serializer.is_valid():
                if serializer.data['generated_token'] == int(data.get("generated_token")):
                    user.is_verified = True
                    user.save()
                    return Response({"user": "verified successfully"})
                else:
                    return Response(
                        {'error': 'The entered token is invalid'},
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
    queryset = WatchList.objects.all()

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.WatchListRetrieveSerializer
        else:
            return self.serializer_class


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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
