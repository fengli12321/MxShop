
from rest_framework import serializers
from .models import ShoppingCart
from goods.models import Goods
from goods.serializer import GoodsSerializer

class ShoppingCartDetailSerializer(serializers.ModelSerializer):

    goods = GoodsSerializer()
    class Meta:
        model = ShoppingCart
        fields = "__all__"

class ShoppingCartSerializer(serializers.Serializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True)
    nums = serializers.IntegerField(required=True, min_value=1, error_messages={
        "min_value": "数量太少",
        "required": "请填写购买数量"
    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]
        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        instance.nums = validated_data["nums"]
        instance.save()
        return instance