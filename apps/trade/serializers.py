import time
from rest_framework import serializers
from .models import ShoppingCart, OrderInfo, OrderGoods
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

class OrderGoodsSerializer(serializers.ModelSerializer):

    goods = GoodsSerializer()
    class Meta:
        model = OrderGoods
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    order_sn = serializers.DateTimeField(read_only=True)
    trade_no = serializers.DateTimeField(read_only=True)
    pay_status = serializers.DateTimeField(read_only=True)

    def generate_order_sn(self):
        from random import Random
        rand_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"), userid=self.context["request"].user.id, ranstr=rand_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"



class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    class Meta:
        model = OrderInfo
        fields = "__all__"