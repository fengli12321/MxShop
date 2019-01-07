from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model


from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializer import GoodsSerializer


User = get_user_model()
class UserFavDetailSerializer(serializers.ModelSerializer):

    goods = GoodsSerializer()
    class Meta:
        model = UserFav
        fields = ('goods', 'id')

class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserFav
        fields = ("user", "goods", "id")
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]

class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%m")
    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "add_time", "id")

class AdressSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = UserAddress
        fields = "__all__"