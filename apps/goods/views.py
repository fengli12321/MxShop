

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .serializer import GoodsSerializer, CategorySerializer, BannerSeralizer, HotSearchSerializer, IndexCategorySerializer

from .models import Goods, GoodsCategory, Banner, HotSearchWords
from .filters import GoodsFilter



class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100
# Create your views here.
class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ['name', 'goods_brief', 'goods_desc']
    ordering_fields = ['sold_num', 'shop_price']


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类数据
    """

    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class HotSearchViewSets(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = HotSearchSerializer
    queryset = HotSearchWords.objects.all().order_by('-index')

class BannerViewSets(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = BannerSeralizer
    queryset = Banner.objects.all().order_by("index")

class IndexCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer