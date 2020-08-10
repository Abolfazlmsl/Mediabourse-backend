from rest_framework import serializers

from bourse.models import User, WatchList, WatchListItem


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'name',
                  'is_verified']
        read_only_fields = ('id',)


class UserSignUpSerializer(serializers.ModelSerializer):

    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['phone_number', 'password', 'generated_token']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        phone_number = self.validated_data['phone_number']
        generated_token = self.validated_data['generated_token']
        user = User(
            phone_number=phone_number,
            generated_token=generated_token,
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class UserPhoneRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone_number', 'generated_token')


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change"""

    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class WatchListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WatchList
        fields = '__all__'
        read_only_fields = ('id', 'user')


class WatchListItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = WatchListItem
        fields = '__all__'
        read_only_fields = ('id',)