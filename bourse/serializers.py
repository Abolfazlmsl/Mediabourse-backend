from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Company, \
    News, \
    UserTechnical, \
    Technical, \
    Webinar, \
    Category, \
    Fundamental, \
    Bazaar, \
    Tutorial, \
    TutorialCategory, \
    TutorialSubCategory, FileRepository, User, WatchList, WatchListItem, Instrumentsel, UserComment, Notification


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'first_name',
            'last_name'
        )


class WatchListSerializer(serializers.ModelSerializer):  # forms.ModelForm

    class Meta:
        model = WatchList
        fields = [
            'id',
            'user',
            'name',
        ]
        read_only_fields = ['id', 'user']

    def validate_name(self, value):
        qs = WatchList.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This WatchList name has already been used")
        return value


class WatchListItemSerializer(serializers.ModelSerializer):  # forms.ModelForm
    company_name = serializers.SerializerMethodField(read_only=True)
    company_english_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WatchListItem
        fields = [
            'id',
            'watch_list',
            'company',
            'company_name',
            'company_english_name',
        ]
        read_only_fields = ['id', 'company_name']

    def get_company_name(self, obj):
        return obj.get_short_name()

    def get_company_english_name(self, obj):
        return obj.get_short_english_name()

    def validate_title(self, value):
        qs = WatchListItem.objects.filter(company=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This company has already been used")
        return value


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id',
            'name'
        )


class InstrumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instrumentsel
        fields = '__all__'


class NewsListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    instrument = InstrumentSerializer(many=False)
    user = UserSerializer(many=False)

    class Meta:
        model = News
        fields = (
            'id',
            'category',
            'instrument',
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


class UserTechnicalSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    instrument = InstrumentSerializer(many=False)

    class Meta:
        model = UserTechnical
        fields = '__all__'


class TechnicalListSerializer(serializers.ModelSerializer):
    """Technical list serializer"""

    class Meta:
        model = Technical
        fields = (
            'id',
            'title',
            'thumbnail',
            'instrument'
        )


class TechnicalRetrieveSerializer(serializers.ModelSerializer):
    """Technical retrieve serializer"""
    user = UserSerializer(many=False)
    company = InstrumentSerializer(many=False)

    class Meta:
        model = Technical
        fields = '__all__'


class WebinarSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    company = InstrumentSerializer(many=False)

    class Meta:
        model = Webinar
        fields = '__all__'


class FundamentalSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    instrument = InstrumentSerializer(many=False)

    class Meta:
        model = Fundamental
        fields = '__all__'


class BazaarSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    instrument = InstrumentSerializer(many=False)

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


class TutorialFileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    file = serializers.FileField()


class TutorialListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tutorial
        fields = (
            'id',
            'title',
            'thumbnail'
        )


class TutorialRetrieveSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    sub_category = TutorialSubCategorySerializer(many=False)
    tutorial_files = TutorialFileSerializer(many=True)

    class Meta:
        model = Tutorial
        fields = '__all__'


class FileRepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FileRepository
        exclude = ['user']


class UserForgetSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField()

    class Meta:
        model = User


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comment model"""

    class Meta:
        model = UserComment
        fields = (
            'id',
            'parent',
            'text',
            'comment_for',
            'like',
            'created_on'
        )


class NotificationListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField()

    class Meta:
        model = Notification
        fields = (
            'id',
            'title',
            'company_name',
            'thumbnail',
            'created_on'
        )


class NotificationDetailSerializer(NotificationListSerializer):

    class Meta:
        model = Notification
        fields = (
            'id',
            'title',
            'text',
            'company',
            'thumbnail',
            'created_on'
        )
        depth = 1
