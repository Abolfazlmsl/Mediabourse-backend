from rest_framework import serializers, validators

from bourse.models import User, WatchList, WatchListItem, Company, Category, News, Basket, UserTechnical, UserComment, \
    Note, Bookmark, RequestSymbol, Instrumentsel


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'first_name',
                  'last_name', 'is_verified', 'picture',
                  'national_code', 'father_name', 'birth_date',
                  'postal_code', 'address']
        read_only_fields = ('id',)


class UserSignUpSerializer(serializers.ModelSerializer):

    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['phone_number', 'password', 'generated_token']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        read_only_fields = (
            'generated_token',
        )

    def create(self, validated_data):
        phone_number = self.validated_data['phone_number']
        generated_token = self.validated_data['generated_token']
        user = User(
            phone_number=phone_number,
            generated_token=generated_token,
        )
        password = self.validated_data['password']
        user.is_active = False
        user.set_password(password)
        user.save()
        return user


class ResendSignUpTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['phone_number', 'generated_token']
        read_only_fields = (
            'generated_token',
        )


class UserPhoneRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone_number', 'generated_token')


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change"""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = [
            'id',
            'title',
            'pic',
            'short_description'
        ]


class InstrumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instrumentsel
        fields = [
            'id',
            'code',
            'name',
            'short_name',
            'exchange',
            'isin',
            'stock',
            'exchange',
        ]


class WatchListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WatchList
        fields = '__all__'
        read_only_fields = ('id', 'user')


class WatchListItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = WatchListItem
        exclude = ['id', 'watch_list']
        depth = 1
        validators = [
            validators.UniqueTogetherValidator(
                queryset=WatchListItem.objects.all(),
                fields=('watch_list', 'company')
            )
        ]


class WatchListRetrieveSerializer(serializers.ModelSerializer):
    item = WatchListItemSerializer(many=True)

    class Meta:
        model = WatchList
        fields = '__all__'
        read_only_fields = ('id', 'user')


class WatchListItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = WatchListItem
        fields = '__all__'
        read_only_fields = ('id', 'user')


class WatchListItemListRetrieveSerializer(serializers.ModelSerializer):
    company = InstrumentSerializer(many=False)

    class Meta:
        model = WatchListItem
        fields = '__all__'


class BasketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = '__all__'
        read_only_fields = ('id', 'user')


class BasketSerializer(serializers.ModelSerializer):
    company = InstrumentSerializer(many=False)

    class Meta:
        model = Basket
        fields = '__all__'


class UserTechnicalSerializer(serializers.ModelSerializer):
    instrument = InstrumentSerializer(many=False)

    class Meta:
        model = UserTechnical
        exclude = ('is_share',)


class UserCommentSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer(many=False)

    class Meta:
        model = UserComment
        fields = '__all__'
        depth = 1


class NoteSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer(many=False)

    class Meta:
        model = Note
        fields = '__all__'
        depth = 1


class BookmarkSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer(many=False)

    class Meta:
        model = Bookmark
        fields = '__all__'
        depth = 1


class InstrumentSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instrumentsel
        fields = [
            'id',
            'code',
            'name',
            'short_name',
            'exchange',
            'isin',
            'stock',
            'exchange',
        ]


class RequestSymbolCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestSymbol
        fields = '__all__'
        read_only_fields = ('id', 'user', 'is_analyzed')


class RequestSymbolSerializer(serializers.ModelSerializer):
    # company = InstrumentSerializer(many=False)

    class Meta:
        model = RequestSymbol
        fields = "__all__"