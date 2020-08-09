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
from .permissions import IsOwner


class UserInfoView(RetrieveUpdateAPIView):
    """Show detailed of user"""
    serializer_class = serializers.UserUpdateSerializer
    authentication_classes = (JWTAuthentication,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class SignUpAPIView(APIView):
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


def is_manager(user):
    return user.groups.filter(name='Manager').exists()


class IsManagerAPIView(APIView):

    def get(self, request):
        user = User.objects.get(phone_number=request.user.phone_number)
        if is_manager(user):
            return Response(
                {
                    'isManager': True,
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'isManager': False,
                },
                status=status.HTTP_200_OK
            )


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
    serializer_class = serializers.WatchListSerializer
    authentication_classes = (JWTAuthentication,)
    queryset = WatchList.objects.all()

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)


class WatchListItemViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.CreateModelMixin):
    serializer_class = serializers.WatchListItemSerializer
    authentication_classes = (JWTAuthentication,)
    queryset = WatchList.objects.all()

    def get_queryset(self):
        return WatchListItem.objects.filter(watch_list__user=self.request.user)