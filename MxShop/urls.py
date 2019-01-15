"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf.urls import url, include
import xadmin
from MxShop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from goods.views import GoodsListViewSet, CategoryViewSet, BannerViewSets, HotSearchViewSets, IndexCategoryViewSet
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSets, LeavingMessageViewSets, AdressViewSets
from trade.views import ShoppingCartViewSets, OrderViewSets, AliPayView
from django.views.generic import TemplateView

router = DefaultRouter()
# 配置goods的url
router.register(r'goods', GoodsListViewSet, base_name="goods")

# 配置goodsCategroy的url
router.register(r'categorys', CategoryViewSet, base_name="categorys")


# 配置verify的url
router.register(r'codes', SmsCodeViewSet, base_name="codes")


# 配置User的url
router.register(r'users', UserViewSet, base_name="users")


#收藏
router.register(r'userfavs', UserFavViewSets, base_name="userfavs")

# 留言
router.register(r'messages', LeavingMessageViewSets, base_name='messages')

# 收货地址管理
router.register(r'address', AdressViewSets, base_name='address')

# 购物车
router.register(r'shopcarts', ShoppingCartViewSets, base_name="shopcarts")

# 热搜
router.register(r'hotsearchs', HotSearchViewSets, base_name="hotserchs")

# 订单
router.register(r'orders', OrderViewSets, base_name='orders')

# 轮播图
router.register(r'banners', BannerViewSets, base_name='banners')

# 首页商品
router.register(r'indexgoods', IndexCategoryViewSet, base_name='indexgoods')

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^', include(router.urls)),
    url(r'^docs/', include_docs_urls("文档title")),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^login/', obtain_jwt_token),
    url(r'^alipay/return/', AliPayView.as_view(), name='alipay'),
    url(r'^index/', TemplateView.as_view(template_name="index.html"), name='index')
]
