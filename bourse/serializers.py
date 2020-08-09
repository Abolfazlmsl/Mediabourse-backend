from rest_framework import serializers

from .models import Company, News, TechnicalUser


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        exclude = ['created_on']


class NewsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = (
            'id',
            'category',
            'company',
            'title',
            'created_on',
            'pic',
            'tag',
            'short_description'
        )


class NewsRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        exclude = ['user']
        depth = 1


class TechnicalUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TechnicalUser
        fields = '__all__'
