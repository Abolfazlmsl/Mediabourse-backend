from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Company, News, TechnicalUser, Technical, Webinar, Category


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'name'
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id',
            'title'
        )


class CompanySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)

    class Meta:
        model = Company
        exclude = ['created_on', 'user']


class NewsListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    company = CompanySerializer(many=False)
    user = UserSerializer(many=False)

    class Meta:
        model = News
        fields = (
            'id',
            'category',
            'company',
            'user',
            'title',
            'created_on',
            'pic',
            'tag',
            'short_description'
        )


class NewsRetrieveSerializer(NewsListSerializer):

    class Meta(NewsListSerializer.Meta):
        fields = '__all__'


class TechnicalUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    company = CompanySerializer(many=False)

    class Meta:
        model = TechnicalUser
        fields = '__all__'


class TechnicalSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    company = CompanySerializer(many=False)

    class Meta:
        model = Technical
        fields = '__all__'


class WebinarSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    company = CompanySerializer(many=False)

    class Meta:
        model = Webinar
        fields = '__all__'
