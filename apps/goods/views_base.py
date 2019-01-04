

from django.views.generic.base import View

from goods.models import Goods
class GoodsListView(View):
    def get(self, request):
        goods = Goods.objects.all()[:10]


        import json
        from django.core import serializers
        json_data = serializers.serialize('json', goods)
        json_data = json.loads(json_data)

        from django.http import JsonResponse

        return JsonResponse(json_data, safe=False)