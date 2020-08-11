from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Company, \
    News, \
    TechnicalUser, \
    Technical, \
    Webinar, \
    Category, \
    Fundamental, \
    Bazaar,\
    Tutorial,\
    TutorialCategory,\
    TutorialSubCategory


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


class FundamentalSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    company = CompanySerializer(many=False)

    class Meta:
        model = Fundamental
        fields = '__all__'


class BazaarSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    company = CompanySerializer(many=False)

    class Meta:
        model = Bazaar
        fields = '__all__'


class TutorialCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TutorialCategory
        fields = (
            'id',
            'title'
        )


class TutorialSubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)

    class Meta:
        model = TutorialSubCategory
        fields = (
            'id',
            'category',
            'title',
            'category_level'
        )


class TutorialSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    sub_category = TutorialSubCategorySerializer(many=False)

    class Meta:
        model = Tutorial
        fields = '__all__'
