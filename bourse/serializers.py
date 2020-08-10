from rest_framework import serializers

from .models import Company, News, TechnicalUser, Technical, Webinar


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


class TechnicalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Technical
        fields = '__all__'


class WebinarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Webinar
        fields = '__all__'
