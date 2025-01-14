import json

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
    TutorialSubCategory, FileRepository, User, WatchList, WatchListItem, Instrumentsel, UserComment, Notification, \
    TechnicalJSONUser, BugReport, NewsPodcast, Article, Tradedetail, InstrumentInfo, TradeCurrent, TradedetailCurrent,\
    Trade


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'first_name',
            'last_name'
        )


class BugReportSerializer(serializers.ModelSerializer):  # forms.ModelForm

    class Meta:
        model = BugReport
        fields = [
            'id',
            'text',
            'email',
        ]
        read_only_fields = ['id']


class InstrumentInfoSerializer(serializers.ModelSerializer):  # forms.ModelForm

    class Meta:
        model = InstrumentInfo
        fields = [
            'id',
            'instrument',
            'volAvg1M',
            'volAvg3M',
            'volAvg12M',
            'created_on',
            'val_support',
            'val_resistance',
            'candle_start_date',
        ]
        read_only_fields = ['id', 'instrument', ]


class TradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = (
            # 'date_time',
            'open_price',
            'high_price',
            'low_price',
            # 'close_price',
            # 'close_price_change',
            'real_close_price',
            # 'real_close_price_change',
            'value',
            # 'buyer_count',
            'volume',
            'trade_count',
            # 'adjusted_close_price'
            # 'instrument_short_name'
        )
        read_only_fields = ['date_time', 'open_price', 'high_price', 'low_price', 'close_price', 'close_price_change'
            , 'real_close_price', 'real_close_price_change', 'value', 'buyer_count', 'volume', 'trade_count'
            , 'adjusted_close_price']


class TradedetailSerializer(serializers.ModelSerializer):  # forms.ModelForm
    trade = TradeSerializer()
    instrument_short_name = serializers.SerializerMethodField(read_only=True)
    instrument_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tradedetail
        fields = [
            'date_time',
            'person_buyer_count',
            'company_buyer_count',
            'person_buy_volume',
            'company_buy_volume',
            'person_seller_count',
            'company_seller_count',
            'person_sell_volume',
            'company_sell_volume',
            'instrument_short_name',
            'instrument_id',
            'trade'
        ]
        read_only_fields = ['date_time', 'person_buyer_count', 'company_buyer_count', 'person_buy_volume',
                            'company_buy_volume', 'person_seller_count', 'company_seller_count', 'person_sell_volume',
                            'company_sell_volume']
        depth = 1

    def get_instrument_short_name(self, obj):
        return obj.instrument.short_name

    def get_instrument_id(self, obj):
        return obj.instrument.id


class TradeCurrentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradeCurrent
        fields = (
            # 'date_time',
            'open_price',
            'high_price',
            'low_price',
            # 'close_price',
            # 'close_price_change',
            'real_close_price',
            # 'real_close_price_change',
            'value',
            # 'buyer_count',
            'volume',
            'trade_count',
            # 'adjusted_close_price'
            # 'instrument_short_name'
        )
        read_only_fields = ['date_time', 'open_price', 'high_price', 'low_price', 'close_price', 'close_price_change'
            , 'real_close_price', 'real_close_price_change', 'value', 'buyer_count', 'volume', 'trade_count'
            , 'adjusted_close_price']


class TradedetailCurrentSerializer(serializers.ModelSerializer):
    trade = TradeCurrentSerializer()
    instrument_short_name = serializers.SerializerMethodField(read_only=True)
    instrument_id = serializers.SerializerMethodField(read_only=True)
    InsreumentInfo = serializers.SerializerMethodField(read_only=True)
    # InsreumentInfo = InstrumentInfoSimpleSerializer()

    class Meta:
        model = TradedetailCurrent
        fields = (
            'date_time',
            'person_buyer_count',
            'company_buyer_count',
            'person_buy_volume',
            'company_buy_volume',
            'person_seller_count',
            'company_seller_count',
            'person_sell_volume',
            'company_sell_volume',
            'instrument_short_name',
            'instrument_id',
            'trade',
            'InsreumentInfo',
        )
        read_only_fields = ['date_time', 'person_buyer_count', 'company_buyer_count', 'person_buy_volume'
            , 'company_buy_volume', 'person_seller_count', 'company_seller_count', 'person_sell_volume'
            , 'company_sell_volume']
        depth = 1

    def get_instrument_short_name(self, obj):
        return obj.instrument.short_name

    def get_instrument_id(self, obj):
        return obj.instrument.id

    def get_InsreumentInfo(self, obj):
        # print(obj.instrument.id, obj.instrument.short_name)
        insInf, is_created = InstrumentInfo.objects.get_or_create(instrument_id=obj.instrument.id)
        obj_json = {
            'id': insInf.id,
            'volAvg1M': insInf.volAvg1M,
            'volAvg3M': insInf.volAvg3M,
            'volAvg12M': insInf.volAvg12M,
            'created_on': insInf.created_on,
            'val_support': insInf.val_support,
            'val_resistance': insInf.val_resistance,
            'candle_start_date': insInf.candle_start_date
        }
        return obj_json


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
    company_full_name = serializers.SerializerMethodField(read_only=True)
    company_english_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WatchListItem
        fields = [
            'id',
            'watch_list',
            'company',
            'company_name',
            'company_full_name',
            'company_english_name',
        ]
        read_only_fields = ['id', 'company_name', 'company_full_name', 'company_english_name']

    def get_company_name(self, obj):
        return obj.get_short_name()

    def get_company_full_name(self, obj):
        return obj.get_name()

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


class ArticleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    pic_url = serializers.CharField(max_length=255)

    class Meta:
        model = Article
        # fields = '__all__'
        fields = (
            'id',
            'category',
            'title',
            'thumbnail',
            'pic_url',
            'text',
            'date',
            'author',
            'tag',
            'hit_count'
        )


class ArticleRetrieveSerializer(ArticleListSerializer):
    class Meta:
        model = Article
        exclude = ('thumbnail',)


class UserTechnicalSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    instrument = InstrumentSerializer(many=False)

    class Meta:
        model = UserTechnical
        fields = '__all__'


class TechnicalJSONUserSerializer(serializers.ModelSerializer):  # forms.ModelForm
    user_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TechnicalJSONUser
        fields = [
            'id',
            'user',
            'user_name',
            'created_on',
            'instrument',
            'title',
            'isShare',
            'data',
        ]
        read_only_fields = ['id', 'user', 'user_name']

    def get_user_name(self, obj):
        return str(obj.user.phone_number)

    def validate_title(self, value):
        qs = TechnicalJSONUser.objects.filter(title__iexact=value)  # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This title has already been used")
        return value


class TechnicalListSerializer(serializers.ModelSerializer):
    """Technical list serializer"""
    user = UserSerializer(many=False)

    class Meta:
        model = Technical
        fields = (
            'id',
            'title',
            'user',
            'thumbnail',
            'instrument',
            'description'
        )


class TechnicalRetrieveSerializer(serializers.ModelSerializer):
    """Technical retrieve serializer"""
    user = UserSerializer(many=False)
    instrument = InstrumentSerializer(many=False)

    class Meta:
        model = Technical
        fields = '__all__'


class WebinarSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    # company = InstrumentSerializer(many=False)

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


class CommentListSerializer(serializers.ModelSerializer):
    """Serializer for comment model"""

    class Meta:
        model = UserComment
        fields = (
            'id',
            'user',
            'parent',
            'technical',
            'fundamental',
            'webinar',
            'news',
            'text',
            'comment_for',
            'like',
            'created_on'
        )
        read_only_fields = ['id', 'user']


class NewsCommentRetrieveSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    reply = serializers.SerializerMethodField()

    def get_reply(self, obj):
        queryset = UserComment.objects.filter(parent_id=obj.id)
        serializer = NewsCommentRetrieveSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = UserComment
        fields = (
            'id',
            'user',
            'parent',
            'text',
            'news',
            'like',
            'reply',
            'created_on',
        )


class NewsListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    instrument = InstrumentSerializer(many=False)
    user = UserSerializer(many=False)
    pic_url = serializers.CharField(max_length=255)

    class Meta:
        model = News
        fields = (
            'id',
            'category',
            'instrument',
            'user',
            'title',
            'date',
            'pic_url',
            'tag',
            'short_description'
        )


class NewsRetrieveSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    instrument = InstrumentSerializer(many=False)
    user = UserSerializer(many=False)
    pic_url = serializers.CharField(max_length=255)
    comment = NewsCommentRetrieveSerializer(many=True)

    class Meta:
        model = News
        fields = (
            'id',
            'category',
            'instrument',
            'user',
            'title',
            'date',
            'pic_url',
            'tag',
            'short_description',
            'comment',
            'description'
        )


class NotificationListSerializer(serializers.ModelSerializer):
    # company_name = serializers.CharField()

    class Meta:
        model = Notification
        fields = (
            'id',
            'title',
            # 'company_name',
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
            # 'company',
            'thumbnail',
            'created_on'
        )
        depth = 1


class NewsPodcastListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPodcast
        fields = (
            'id',
            'title',
            'thumbnail'
        )


class NewsPodcastDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPodcast
        fields = '__all__'

