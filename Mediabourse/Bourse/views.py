from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .rest_api.serializers import UserSerializer
from rest_framework import status, generics, viewsets
from .rest_api.serializers import ChangePasswordSerializer
from .rest_api import serializers
from .models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404


class StockCreate(viewsets.ModelViewSet):
    """
    Manage Stock
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = serializers.StockSerializer
    queryset = Stock.objects.all()

    def retrieve(self, request, *args, **kwargs):
        queryset = Stock.objects.all()
        stock = None
        if not kwargs['pk'].isnumeric():
            stock = get_object_or_404(queryset, symbol=int(kwargs['pk']))
        serializer = serializers.StockSerializer(stock)
        return Response(serializer.data)


class WatcherCreate(viewsets.ModelViewSet):
    """
    Manage Watcher
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = serializers.WatcherSerializer
    queryset = Watcher.objects.all()

    def retrieve(self, request, *args, **kwargs):
        queryset = Watcher.objects.all()
        watcher = None
        if kwargs['pk'].isnumeric():
            watcher = get_object_or_404(queryset, user_id=int(kwargs['pk']))
        serializer = serializers.CompanySerializer(watcher)
        return Response(serializer.data)


class CategoryCreate(viewsets.ModelViewSet):
    """
    Manage Category
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()


class CompanyCreate(viewsets.ModelViewSet):
    """
    Manage Company
    """
    # def post(self, request):
    #     pass
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = serializers.CompanySerializer
    queryset = Company.objects.all()

    # def list(self, request, *args, **kwargs):
    #     queryset = Company.objects.all()
    #     serializer = serializers.CompanySerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    def retrieve(self, request, *args, **kwargs):
        queryset = Company.objects.all()
        company = None
        if kwargs['pk'].isnumeric():
            company = get_object_or_404(queryset, id=int(kwargs['pk']))
        elif not kwargs['pk'].isnumeric():
            company = get_object_or_404(queryset, symbol=str(kwargs['pk']))
        serializer = serializers.CompanySerializer(company)
        return Response(serializer.data)


class UserCreate(APIView):
    """
    Manage User.
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
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
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
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
