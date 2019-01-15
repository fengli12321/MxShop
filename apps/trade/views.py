from datetime import datetime

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly


from .models import ShoppingCart, OrderInfo, OrderGoods
from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer, OrderSerializer, OrderDetailSerializer
from MxShop.settings import private_key_path, ali_pub_key_path

class ShoppingCartViewSets(viewsets.ModelViewSet):
    serializer_class = ShoppingCartSerializer
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    lookup_field = "goods_id"
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCartDetailSerializer
        else:
            return ShoppingCartSerializer


class OrderViewSets(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    authentication_classes = (SessionAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        else:
            return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            shop_cart.delete()

        return order


from rest_framework.views import APIView
from utils.alipay import AliPay
from rest_framework.response import Response
class AliPayView(APIView):
    def get(self, request):
        process_dict = {}
        for key, value in request.GET.items():
            process_dict[key] = value
        sign = process_dict.pop("sign", None)

        alipay = AliPay(
            appid="2016092400587748",
            app_notify_url="http://129.28.107.12:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://129.28.107.12:8000/alipay/return/"
        )
        verify_result = alipay.verify(process_dict, sign)
        if verify_result is True:
            order_sn = process_dict.get('out_trade_no', None)
            trade_no = process_dict.get('trade_no', None)
            trade_status = process_dict.get('trade_status', None)
            exited_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for exited_order in exited_orders:
                exited_order.pay_status = trade_status
                exited_order.trade_no = trade_no
                exited_order.pay_time = datetime.now()
                exited_order.save()
            return Response('success')


    def post(self, request):
        process_dict = {}
        for key, value in request.POST.items():
            process_dict[key] = value
        sign = process_dict.pop("sign", None)

        alipay = AliPay(
            appid="2016092400587748",
            app_notify_url="http://129.28.107.12:8000/alipay/return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://129.28.107.12:8000/alipay/return/"
        )
        verify_result = alipay.verify(process_dict, sign)
        if verify_result is True:
            order_sn = process_dict.get('out_trade_no', None)
            trade_no = process_dict.get('trade_no', None)
            trade_status = process_dict.get('trade_status', None)
            exited_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for exited_order in exited_orders:
                exited_order.pay_status = trade_status
                exited_order.trade_no = trade_no
                exited_order.pay_time = datetime.now()
                exited_order.save()
            return Response('success')

