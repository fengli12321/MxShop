import os
import sys


pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MxShop.settings')


import django

django.setup()


from goods.models import GoodsCategory

from db_tools.data.category_data import row_data


for lev1_data in row_data:
    lev1_instance = GoodsCategory()
    lev1_instance.name = lev1_data["name"]
    lev1_instance.code = lev1_data["code"]
    lev1_instance.category_type = 1
    lev1_instance.save()

    for lev2_data in lev1_data["sub_categorys"]:
        lev2_instance = GoodsCategory()
        lev2_instance.name = lev2_data["name"]
        lev2_instance.code = lev2_data["code"]
        lev2_instance.parent_category = lev1_instance
        lev2_instance.category_type = 2
        lev2_instance.save()

        for lev3_data in lev2_data["sub_categorys"]:
            lev3_instance = GoodsCategory()
            lev3_instance.name = lev3_data["name"]
            lev3_instance.code = lev3_data["code"]
            lev3_instance.parent_category = lev2_instance
            lev3_instance.category_type = 3
            lev3_instance.save()